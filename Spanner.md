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

## Asdf















# 