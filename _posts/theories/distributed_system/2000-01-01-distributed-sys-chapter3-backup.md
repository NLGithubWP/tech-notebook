---
title: distributed system chapter3 primary/backup
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [distributed database]
---

# Question

Does the primary need to forward reads to backups? or can we do fast reads in primary/backup replication? 

`No, it cause stale read problem`

it is not linearizable but it is sequentially consistent. 


![image-20220204230112657]({{ site.baseurl }}/img/a_img_store/image-20220209173603528.png)


`考虑如下情况，A连不上view server， B成了primary， client1 知道了这个结果，发送w到了B，但是client2还不知道，仍然发送R给了A， 如果A把读同步到B，B会发现当前的view和A的view不一致，所以拒绝，A收到拒绝后，让client retry，这样不会有错误的结果发生。`

# Basic Operation

Clients only send operations (Put, `Get`) to primary.

Primary decides `on order of ops` and forwards sequence of ops to backup.

Backup performs ops in same order (hot standby), Or just saves the log of operations (cold standby).

After backup has saved ops, primary replies to client.

# Challenge

1. How to handle no-deterministic operations?
2. What state should be transfered (operations or contents of memory) ?
3. How to provide strong consistency (linearizability) ? 
4. `How to handle server failures to make new primary has up-to-data state ?`
5. How to prevent split-brain ? 

# Solutions

## View service (single point failure)

   ![image-20220204230112657]({{ site.baseurl }}/img/a_img_store/image-20220204203014472.png)


View server `detect failure`, `handle failure` and `manage servers`

### **basic operation**

- view forms a sequence in time
- `detect failure`
  - The view service maintains role for each node
  - Each server periodically pings (Ping RPC) view server. If n pings is missing, then the node is considered to be dead.
- `handle failure`
  - On primary failure, one backup => primary, one idle => backup (init with primary's state), primary state transfer, view server get ack from primary and then declare a new view.
  - On backup failure, one idle => backup, primary state transfer, view server get ack from primary and then declare a new view.
- `manage servers`
  - Any server can ping view server. 
  - view service maintain 2 server (one primary and one backup), extras are “idle” which can be promoted to backup.

### **Rules in implementation**

简而言之， 

1. primary 刚选上，要做`state transfer`
2. Primary只能从backup中选， primary在返回client前等待backup同步。 
3. Backup只接受同view的primary请求， Backup不接受client的request。 
4. state transfer 期间系统不可用。
5. 出错后，View server等待primary的state transfer 确认才更新本地server集群role。在此之前，primary和backup都不能跟新。

In detail

0. Do **not** ask view server on every request in client side.

0. View server declare a new view if and only if it receive ack from primary. And primay send ack <Ping, viewNum+1> to view server(with viewNum) after `finishing state transfer`. 

   *=> `make sure new primary has up-to-data state`*

1. Primary in view i+1 must have been backup or primary in view i.

   *=> 只能从backup或primary挑选新的primary，不能从idle中选，否则会引起`split-brain`*

2. Primary must wait for backup to accept/execute each op before replying to client

   *=> `strong consistency`, write to Primary, primary failed to send to backup, primary return to client,* *primary die, client read from backup, backup doesn't have this data.* 

3. Backup must accept forwarded requests only if the view is correct

   *=> `prevent split-brain` eg,. backup B get request from previous primary A after A fail and B become new primary, if B accepts it and reply to A, then A can return to client. but if B also fails, C become primary, C may return different res to client*

4. Non-primary must reject client requests

   => `strong consistency.`

5. Every operation must be before or after state transfer

   => `strong consistency`, during state transfer, the system is unavailabe

   ![image-20220204230112657]({{ site.baseurl }}/img/a_img_store/image-20220204224732085.png)


### **Architecture**

![image-20220204230112657]({{ site.baseurl }}/img/a_img_store/image-20220204230112657.png)

# Project Design

## View Server

关键点：

1. 挂了可以切换（backup view 相同的时候），可以暂时改变view，然后等待ack。
2. 只有primary的ack到了，才能增加新的backup，并且改变view

some test case rules

1. viewserver init with (null, null, viewNum = 0)
2. if primary = null(must be startup), view(0) => newView(1) 
3. if primary acked (1), backup come, view(1) => newView(2)
4. if primary not acked (1), backup come, primary acked, view => newView(2)
5. primary fail, 
   - primary/backup at view(2) = currentView(2) 
   - primary now fail, backup => primary, view => newView(3)
6. primary fail,
   - primary/backup at view(2) = currentView(2) 
   - primary now fail, backup => primary, view => newView(3)
   - New primary acked(3), backup come, view => newView(4)
7. primary fail, 
   - primary/backup at view(2) = currentView(2) 
   - primary now fail, backup => primary, idle => backup, view => newView(3)
8. primary fail,
   - primary at view(1), 
   - backup come, view => newView(2)
   - primary not ack(2).
   - primary now fail, cannot use this backup. but keep it.
9. backup fail, 
   - primary/backup at view(2) = currentView(2) 
   - backup now fail, remove it, view => newView(3)
10. primary fail,
    - primary/backup at view(2) = currentView(2) 
    - primary now fail, backup => primary, idle => backup, view => newView(3)
    - New primary now fail before acked, cannot use this backup. 
11. idle server fail,
    - primary registered
    - Idle come, primary/idle fail. idle is deleted
    - primary restart and ack, view(0) => newView(1)
12. Cc
    - primary registered
    - primary fail, view(1) <=> view(1)
    - primary acked(1)
    - `all server fail, view(1) <=> view(1)`
    - backup come, view => newView(2)
    - primary restart and ack, view(2) <=> view(2)
    - idles timeout, view(2) <=> view(2)
    - `all server fail, view(2) <=> view(2)`





