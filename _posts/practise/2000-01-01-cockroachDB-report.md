---
title: cockroachDB-report
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [practise]
---

## 1. Allocated tasks

xingnaili: Implement the first 4 transcations in driver for both workloads, do some optimizaitons. and cluster settings

Daifei: Implement the last 4 transcations in driver for both workloads, do some optimizaitons. and cluster settings

## 2. Completed tasks

### cluster setting

1. install and run cockraochDB cluster on servers

### schema design 

1. design the schema for workloadA and B
2. De-normalization to faciliate reads workloads
3. Build indexs on each table, for write heavy transaction, use UUID as primary key to avoid hot pot
4. For table with many read-only operations over the application, like table "item", we manually split it to 5 ranges.
5. Assign frequently updated column to a single family for each table
6. Enable multiple advanced setting like experimental_enable_hash_sharded_indexes, load-splitting threshold 

### Driver implementation

1. Analys the each table's reques load on 8 transactions. 
2. Implemented 8 transactions
3. Do some optimizations based on following rules:
   1. Make sure each sql use indexs, avoid full-scan
   2. Avoid multiple client-server exchanges per transaction, group select, insert etc together in single SQL, using "with..."
   3. For insert operation, use batch insert in single sql.
   4. For update and then select scenario, using returing keyword
   5. For read-only tables, try with "follower_read" but failed. It ask for licences
4. Record the evluation matrix, including number of transactions, latency, throughput etc

## 3. In-progress tasks

1. Write the script to launch multiple instances of driver on different servers and test performance
2. Tunning configurations to make the workload more balance
3. Try to find some settings such that it only facilitate either read or write. And use it to distinguished the driver or schema design between workloadA and workloadB.