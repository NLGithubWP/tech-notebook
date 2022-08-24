---
title: distributed system solution2
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [distributed database]
---

# Solutions of 2

## Solution of Question 1

### solution of (a)  

If the top server crash, then the new leader election process will begin. 

The leader election has two rules

- Leader must has all committed logs. 
- Leader has most **up-to-date** log contains all committed entries. 

In this example,  there are 7 servers, so the majority is 4. 

We could see the unique logs labeled with (1,1), (2,1), (3,1), (4,4), (5,4), (6,5), (7,5), (8,6), (9,6) have been replicated to majority of servers. So they can be committed. 

As for replica (a): 

- server a can also be elected at the beginning, it can receive votes from a, b, c, e, f. 

  But when it send AppendEntries RPC to server d, server d founds the term in the RPC is smaller than the d's current term, then the d rejects the RPC and continues in candidate state. 

  So finally, f will win the election and become leader. Server a will convert back to follower. 

As for replica (d): 

- server d has all committed logs and two un committed logs (11, 7) and (12, 7). It has most up-to-date log. 

  So it can be elected, it can receive vote from a,b,c,d,e,f.

As for replica (e): 

- It **cannot** be the leader since it does't have all commited logs. And even if it boardcast to all server.  it can only receive vote from b, e, f. Not majority. 

As for replica (f): 

- It **cannot** be the leader since it does't have all commited logs. And even if it boardcast to all server.  it can only receive vote from f.

### solution of (b)

This is safe to do so. 
The leader will send AppendEntries RPC as heartbeat message. And the AppendEntries PRC includes the preLogTerm and PreLogIndex.  Follower will verify if above match with local log's term and index.  If not then follower reply false.  Leader will decrement the nextIndex and retry until the follower reply true. 

Which means all logs after PreLogIndex is inconsistency and will be overwritten.  So it's safe to delete all after PreLogIndex.

## Solution of Question 2

The answer dependes on how the replica extends the lease and when lease expired.  If each replica can extends lease as long as it can connect to majority,  Then the solution of allowing every replica to serve read request independently is safe and it can guarantee linearizability. 

In this protocol, the leader commits after receiving ack from **`ALL`** replica. Which means once operations are committed, all servers have it. 

Suppose the network partition happens,  servers are divided into two groups.  client 1 write to one group while client 2 read from other group.  client 1 cannot write successfully since leader in either group cannot talk to servers in another group. 

## Solution of Question 3

### solution of (a). 

Large record append may cross chunk. 

For example, if one client A write a file across two chunks, namely chunk a and chunk b.  Chunk a has primary p, while chunk b has primary d. Now if client B write same file and different contents. 

Now primary p could store client A's content while primary b store client B's contents. Which break the correctness. 

### solution of (b). 

If a write fails at one of the secondaries, the client re-tries the write. That will cause the data to be appended more than once at the non-failed replicas.

### solution of (c). 

When client A write to GFS, the data buffer will be written to all replicas. After all replica has the buffer, client can inform replica to commit the change in buffer. Now if primary just commit and backup replica fail to commit. Then client need retry. 

Now if another client read it, the client can read from primary. 

## Solution of Question 4

Read-only transaction don't need add lock. It's safe for serializability if we add `timestamp` 

The reason is read-only transaciton doesn't modify the system status.  

In implementation, when the data is being modified by one client, the data is labelled as "unreadable." and the read-only transaction can read the stable version of the data (timestamp data).

But if there no timestamp or WAL, Dirty read may happens. For example, one transaction contains many writes. And after writting done, user decided to abort.  Since the data is all written in database. Before the data is deleting according to abort request, read-only may read them. It cause dirty read. 

## Solution of Question 5

### solution of (a):

 They use public-key cryptography to sign all messages, so no one can impersonating other nodes. 

- When client send to primary, The message is signed. 

- When primary send pre-prepare message, primary sign the D(m) hash of message

- When backup send prepare message, backup sign the message.

### solution of (b)

The replicas will exchange information about the operations received from primary by sending prepare messages. 

Once a server has received 2f `matching` prepares and associated pre-prepare request, the server has prepare certificate, After that, each server will send commit message to all other replicas.  Once a server has 2f+1 matching commits. it has commit certificates. Since replica only send commit message after getting prepare certificates. A commit certificate means every 2f+1 servers has at least one non-faulty node with prepare certificate. 

If the faulty primary send totally different message to each replica, then the replica cannot make progress. Then the the faulty primary will timeout later and new primary will elected. 

### solution of (c)

No , this is not correct. 

The commit phase of the protocol is to make sure honest server has the prepare certificate. 	

If one replica receives prepare certificates, but it failes. While others don't have such certificate.  Then the system cannot make progress, and cannot decides what operations is in current slot. `So it 's not safe to execute the cmd after receiving the prepare certificates.` 

To make sure enough replicas has certificates. We need another rounds of communications - commit phase.

​	

​	

​	





