---
title: cockroachDB-opt
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [practise]
---

# 1. Schema design (avoid hotpot)

## Relations

Database -> schema -> (tables, views, sequences)

## Schema best practices

If need multiple tables with same name, do so in different schema in same DB

use **schema_name.table_name** to access table

Make transactions smaller by operating on less data per transaction. This will offer fewer opportunities  for transactions' data access to overlap.

[Split the table across multiple ranges](https://www.cockroachlabs.com/docs/v21.1/split-at) to distribute its data across multiple nodes for better load balancing of some write-heavy workloads.

```sql
SHOW RANGES FROM TABLE users
```

![image-20211028154031616](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154031616.png)

## Table best practices

### Create tables:

```sql
CREATE TABLE database_name.schema_name.table_name
```

### Create Columns:

![image-20211028154306793](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154306793.png)

Values exceeding 1MB can lead to write amplification（写放大） and cause performance degradation

### Set index (one or more columns )properly:

1. Must be **unique and not-null values**

2. Set to all **col used for sorting or filter** (=,in )

3. Use storing to store **hot data cols in index**, and also store join key.

   ![image-20211028154437616](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154437616.png)

4. l Avoid **define pk over a single column of sequential data, eg. auto-incrementing INT or timestamp value**

5. l If must define in sequential keys, use hash-sharded index. 

   Hash-sharded indexes distribute sequential traffic uniformly across ranges, eliminating single-range hotspots and improving write performance on sequentially-keyed indexes at a small cost to read performance.

   ![image-20211028154505841](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154505841.png)

   ![image-20211028154513220](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154513220.png)

6. When possible, define primary key constraints over multiple columns (i.e., use composite primary keys).

   The first col is well-distributed across nodes, and second col can be monotonically increasing pk 

7. l For single-column pk, use UUID, gen_random_uuid() function, which ensure the pk value will be unique and well-distributed across a cluster

   **这个uuid无法用于查询，但是可以用于多个表的join**

   ![image-20211028154559441](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154636919.png)

Add proper column constraints

![image-20211028154636919](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154636919.png)

Secondary index:

​	Unique constrain will set se-index automatically

## Advanced schema design

### Computed cols

Useful when table is frequently sorted

![image-20211028154732484](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154732484.png)

![image-20211028154736635](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028154736635.png)

### Column families

reduce the number of keys stored in the key-value store, resulting in improved performance during [INSERT](https://www.cockroachlabs.com/docs/v21.1/insert), [UPDATE](https://www.cockroachlabs.com/docs/v21.1/update), and [DELETE](https://www.cockroachlabs.com/docs/v21.1/delete) operations.

Assign frequently updated col to a single family

https://www.cockroachlabs.com/docs/v21.1/column-families

### Partial index

Add index to part of rows and cols

### Spatial index

### Multiple region

# 2. Write data/read data

## Insert

Batch multiple rows in one multi-row insert statement, use batch (10,100, 1000)

Do not include multi-row insert statements with an explicit tx

## Update

Must use where.

Use batch-update loop to update many rows (https://www.cockroachlabs.com/docs/v21.1/bulk-update-data)

Wrap the update with retry (https://www.cockroachlabs.com/docs/v21.1/error-handling-and-troubleshooting#transaction-retry-errors)

## Follower read 

https://www.cockroachlabs.com/docs/v21.1/follower-reads.html

Follower reads are a mechanism that CockroachDB uses to provide faster reads in situations where you can afford to   read data that may be slightly less than current (using [`AS OF SYSTEM TIME`](https://www.cockroachlabs.com/docs/v21.1/as-of-system-time))

Requirements

1. Read latency is low, but write latency is higher
2. Read can be historical (4.8 second or more in past)
3. Available during region failure

# 3. Manage Txs

![image-20211028155026069](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028155026069.png)

![image-20211028155032359](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028155032359.png)

## Retry:

System automatic retry

​	Require the insert/update/delete without ”returning”, and have small returned 	result size.

​	If returned result is greater than 16kb, cannot retry

Client side retry:

![image-20211028155113030](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211028155113030.png)

## Nested tx

Can rollback to any position in sub tx

# 4. Optimize performance

https://www.cockroachlabs.com/docs/v21.1/make-queries-fast.html

https://www.cockroachlabs.com/docs/v21.1/performance-best-practices-overview#understanding-and-avoiding-transaction-contention

## Avoid transaction contention

### Contention

1. Tx operates on **same range,** but different index key value, limited by single node hardware
2. Tx operates on **same index key values**, will be more strictly serialized to obey Tx isolation semantics

### Multiple strategies

1. Use proper index to distribute the range to multiple nodes
2. Make tx small
3. Avoid multiple client-server exchanges per transaction, group select, insert etc together in single SQL
4. Select for update for scenario of read and then update
5. User upsert when replacing values in row
6. Do normalization to the table
7. If the application strictly requires operating on very few different index key values, consider  using [ALTER ... SPLIT AT](https://www.cockroachlabs.com/docs/v21.1/split-at) so that each index key value can be served by a separate group of nodes in    the cluster.

