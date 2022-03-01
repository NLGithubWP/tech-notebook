# Solutions of 1

1. (a):

Lamport Clock could incur some unnecessary clock logic, in this problem, I suppose we don't consider the Lamport clock but only consider Partial Ordering. We have following.

​	Happens before E: (A, D)

​	Happens after E: (H, I, C, F)

​	Concurrent E: (B, G)

1. (b):

   WIth Lamport clock, we could define the total order of events. 

<img src="imgs/image-20220228211149799.png" alt="image-20220228211149799" style="zoom:50%;" />



​	As shown in the figure, 

​	A=1, B=3, C=10, D=1, E=4, F=6, G=1, H=7, I=9

1. (c):

   <img src="imgs/image-20220228214152153.png" alt="image-20220228214152153" style="zoom:50%;" />

​	As shown in Figure, 

​	A=(1,0,0), B=(3,0,0), C=(5,4,4), D=(0,1,0), E=(2,3,0), F=(2,5,0), 

​	G=(0,0,1), H=(2,4,3), I=(2,4,5)

# Solutions of 2

2. (a)

`Q: How does NFS ensure client updates to the file system are not lost on a server crash?`

- Whenever a client issues a write request, the server must guarantee that all modified data is safely on disk before the write returns. If the server crash before sending back the response, then the client will just retry, the server will respond to the retry request after reboot. 
- If the server crash after sending back the response, then the client operate normally.
- To the client, server failure is just a delay. 

`Q: How does NFS handle client retries when the operation is already executed?`

- This retry causes no problem for idempotent operations. 
- In fact, one of the biggest features of NFS is that almost all operations are idempotent, one that can be executed many times with the same overall effect as if it were executed only once.
- NFS idempotent NFS operations are read/write/lookup. Non-Idempotent NFS operations is mkdir.

2. (b)

`Q: How does Sprite ensure consistency of file data when multiple clients are concurrently reading from and writing to a file?`

- If a file is ever open simultaneously on several clients and at least one of them is writing the file, then the server notifies each of the clients and insists that they not cache the file; all read and write operations must be passed through to the server, where they are applied to a single copy of the file in the server’s cache. 
- If a client has a cached copy of a file, but the file isn’t open on that client, then the client will not be notified if other clients modify the file; stale data will remain in its cache. However, that data cannot be used until the file is opened. When the client makes an open request to the server, the server returns a version number for the file. This version number will not match the version associated with the stale data, so the file will be purged from the client’s cache. Thus Sprite provides perfect file consistency: each read operation is guaranteed to return the most recently written data for that file, regardless of where and when the file is read and written.

# Solutions of 3

3. (a)

This is not sequential consistency, in order to satisfy P2, Write(a) must scheduled after Write(b), but P3 requires read(a) and then read(b). This is contradict

3. (b)

This satisfies sequential consistency, the server could schedule as flowing:

w(a) r(a) w(c) r(c) w(b) r(b)

3. (c)

This doesn't satisfy linearizability, because r(b) must between w(a) and r(a). 

# Solutions of 4

4. (a)

   This is not valid, according to `Paxos P2`, if value a is chosen by the majority (A1 and A2), then any proposal is chosen by any acceptor must include value a, but A3 has value b. This contradicts Paxos P2.

4. (b)

   This is valid, and the message sequence could be as follow:

   - Proposer issues `Prepare request` with 1 to all acceptors
   - All acceptors replied and none of them has accepted any proposal.
   - Proposer then issue `accept request` with (1, a) to all acceptors
   - According to `Paxos P1`, A2 accepts it as this is the first proposal A2 received.
   - Now A1 and A3 fails and didn't receive it.
   - A1 and A3 restart. 
   - Proposer didn't receive response of accept request, so it propose a new proposal with number 2
   - Proposer issues `Prepare request` with 2 to all acceptors.
   - According to P2c.(a) majority (A1, A3) didn't accept any proposal numbered less than 2. 
   - Proposer then issue `accept request` with (2, b) to all acceptors.
   - According to `Paxos P1`, A1 and A3 accept it as this is the first proposal A1 and A3 received.
   - The message is delayed to A2 or A2 fails.
   - Proposer received the majority (A1 and A3) of responses.
   - (2, b) is chosen.

4. (c)

   This is valid, 

   - Assume when proposal number = 1, only A1 accepts it and others didn't receive the message.
   - Assume when proposal number = 2, only A2 accepts it and others didn't receive the message.
   - Now A3 back to the line.
   - According to `Paxos P2c.(b),` the majority(A1, A3) has the situation where A1 accept (1, a) and A3 accept nothing, and the highest-numbered proposal accepted by acceptor in this majority is (1, a), value is a. 
   - Proposal issues `Prepare request to A1 and A3`
   - proposer issues `Accept request` to A1 and A3 with a new proposal with (3, a).
   - A3 accepts it, but A1 misses it. 
   - Now the whole system remains at A1: (1, a), A2: (2, b), A3: (3, a)

4. (d)

   This is not valid,

   - When proposal number = 3, the proposer must firstly issues `prepare request` to the majority, 
   - Proposer must wait until the majority of acceptor response.
   - In this situation, the majority can be (A1, A2) or (A2, A3) or (A1, A3)
   - If the majority is (A1, A2), the proposal accepted by acceptors with the biggest proposal number is (2, b) so the proposer can only issue (3,b)
   - A3 could accept nothing or accept a or accept b.
   - No matter what A3 currently is, proposal can only issue proposal with value selected from (a, b)
   - value c is impossible.

# Solutions of 5

