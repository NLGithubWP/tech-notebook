2021-10-01 [NSDI-2012] Spanner Google’s Globally distributed database

# Abstract

# 1. Introduction

# 2. Implementation

## Spanserver Software Stack

![image-20211012120142565](imgs/image-20211012120142565.png)

**Tablet:** Each server is responsible for between 100 and 1000 instances of data struct, called **tablet**, which is the kv pair as follow, Where spanner assigns **timestamp to data**, which is more like a **multi-version database**.

Spanner tablet is a container that may encap- sulate **multiple partitions of the row space**

```python
(key:string, timestamp:int64) → string
```

Table's state is stored in **B-tree-like files** and **write-ahead log**, all on DFS **Colossus**

Log each Paxos write twice, onece in tablet's log, and once in Paxos log. Write applied by Paxis in order. The implementation of Paxos is **pipelined**, so as to improve Spanner’s throughput in the presence of WAN latencies, <u>(sequential write?)</u>

Write must go to leader, but read can access from underlying tablet at any replica that is **sufficiently up-to-data** <u>(prefix consistency?)</u>

Each raplica leader has a **lock table** to implement concurrency control (**2PL**). It maps ranges of keys to lock states.  Each replica leader also has a **transaction manager** to support distributed transaction (**2pc**)

If only use **one** **Paxos** **group**, **it bypass the transaction manage**r because the lock table and Paxos together provide A.

**State of each transaction manager** is **also stored in underlying Paxos group and is replicated.**

## Directories and Placement

![image-20211012135203429](imgs/image-20211012135203429.png)

**Directory:** **a set** of contiguous **keys** with same prefix. 

​	It enable user to control locality of their data more carefully.

​	All data in same diectory has same replication configuration

**Move data**

​	between Paxos groups, directory by directory

​	To shed load from a Paxos group, eg, put directories that are frequently accessed together into the same group(<u>why?)</u>

​	To move a directory into a group that closer to accessors

​	50MB directory can be moved in a few seconds.

​	"Movedir" task run on background and it will use a single transaction to aotmically update related metadata after moving all data.

Spanner will shard a directory into multiple *fragments* if it grows too large. Fragments may be served from different Paxos groups	

## Data model 

![image-20211012164442833](imgs/image-20211012164442833.png)

Spanner exposes chematized semi-relational tables, query languages, and general purpose transactions.

Running 2pc over Paxos mitigates the availability problems.(<u>why</u>?)

Each dataset must be partitioned by clients into one ore more hierarchies of tables. The table at the **top of it is directory table**. 

**directory = Each row in directory table with key K + rows in descendant tables which starts with K**.

# 3. True Time

![image-20211012215144713](imgs/image-20211012215144713.png)

TrueTime is implemented by a set of *time master* machines per datacenter and a *timeslave daemon* per machine. All masters’ time references are regularly compared against each other.

**Time Master** has GPS receivers and it will advertise a slowly increasing time uncertainty

**timesalve daemon** polls a variety of master (of different data center) to reduce vulnerability to errors from any one master. 

# 4. Concurrency Control

![image-20211012221740708](imgs/image-20211012221740708.png)

True time is used to guarantee the correctness on concurrency control.

## Timestamp Management

A client can either specify a timestamp for a snapshot read, or provide an upper bound on the desired timestamp’s staleness and let Spanner choose a timestamp

### Paxos Leader Leases

When a replica receives quorm of votes, it becomes a leader and each spanner;s leader can live 10 seconds.

Leader extends it's lease on a successful write and leader requests lease-vote extension if it is near expiration

**A leader's lease interval:** the time duration when a replica is a leader. 

For **each Paxos group**, each Paxos leader’s lease interval is disjoint from every other leader’s.

A leader can also abdicate, but it must make sure TT.after(S_max)= True, where the S_max is maximum **timestamp** used by a leader. 

### Timestamps => RW Transactions

Isolaton of RW is guranted by using 2PC.

Spanner assigns it the timestamp that **Paxos assigns to the Paxos write that represents the transaction commit.** (use the time when the Paxos write happens triggered by commit.)

In each Paxos group, spanner leader assigns timestamps to Paxos write in monotonically increasing order. Since the lease interval is disjointness, the timestamp is in monotonically increasing order even across leaders. 

When a timestamp is assigned to a transaction, S_max is updated. 

**External consistency invariant**: If start time of T2 is after commit time of T1, then **commit timestamp of T2** must greater than **commit timestamp of T1**.

**Proof:**

**e_start:**  transaction is started, probably counted on client side.

**e_commit:** transaction is commited

**e_server:** transaction is sent to coordinator leader (server )

<img src="imgs/image-20211012232357062.png" alt="image-20211012232357062" style="zoom:30%;" />

1. **start**

   The coordinator leader for a write tx T_i will assign a **commit timestamp** <= TT.now().latest and >= e_server

2. **commit wait**

   other tx cannot see T_i's update until TT.after(S_i) = true. (if the true time is definitely  greater than commit time of T_i, other tx can see it.)

<img src="imgs/image-20211012234129177.png" alt="image-20211012234129177" style="zoom:40%;" />

### Serving Reads at a Timestamp

Each replica tracks a value - safe time T_safe, which is maximum timestamp at which a replica is up-to-date. (It promises T_safe is up-to-date). Replica can satisfy if t <= T_safe









**Read-Only Tx**: 

1. execute at **system-chosen timestamp** without locking, so it is not blocking any write. 
2. can be executed on any replica which is sufficiently up-to-data
3. 

















# 