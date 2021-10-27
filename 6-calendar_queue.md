Programmable Calendar Queues for High-speed Packet Scheduling

# Introduction

Dynamic priority is required in network scheduling algorithms 

## Current Problems:

1. Switches schedule package is mostly based on coarse-grained queue-level priorities, which is  **not sufficient** to support a broad class of scheduling algorithms that require the **priorities of packets to change as a function of the time** it has spent inside the network.
2. **Switch-level support** for **multiple fine-grained priority levels** can help realizaiton of the scheduling algorithms. But still has challenges. 
   1. implementing strict and fine-grained priority levels is expensive
   2. Switch-level support for priorities does not allow for dynamic changes to the priority of a packet during its stint inside the switch buffer

## Solutions:

Introduce calendar queue abstraction, which is fit for scheduling algorithms which not only require prioritisation but also perform dynamic escalation of packet priorities. 

# Background

## Reconfigurable switches

Assume that the **programmable** **scheduling** is used in conjunction with a reconfigurable switch. eg Reconfigurable Match Table (RMT) model:

1. Package arrives at the switch
2. Header fileds are extracted via **user-defined programmable** parser
3. Header fileds are passed into pipeline of user-defined **programmable** M+A stages. 
4. Each stage match on a subset of extracted headers and perform simple process on header 

Switch also provide several hardware features:

​	Stateful memory, computation primitives, the ability to recirculate or generate special datapath packets using *timers*

Switch metadata:

​	queue lengths, congestion status, and bytes transmitted, can also be used in packet processing

## Traffic Manager

Responsible for two tasks

1. Buffering packets when **many input ports** is trying to **send packets to the same output port** simultaneously

   Each output port has **a fixed number FIFO buffer**. 

   Once a packet is transmitted from **ingress buffer** to **FIFO queue**, it cannot be dropped. 

2. Schedule packets at each output port and so other server can receive it. 

   Since each output port has multiple FIFO buffer, TM uses a combination of factors to determine which queue to dequeue from.

   1. Each queue has a priority
   2. Within a priority level, queues are scheduled in weighted round-round robin order. 
   3. Each queue can be limited to a maximum rate, and can be moved or paused. 

TM maintains each queue's status such that TM can use them to perform buffering and scheduling

## Programmable Scheduling (prior work)

Recent proposals for programmable scheduling propose additional switch hardware in the TM **to make the scheduling decision programmable**.

PIFOs enable programmable scheduling by using a programmable **priority queue** to express custom scheduling algorithms. And the rank determines the packet’s order in the priority queue.

# Packet Scheduling using Programmable Calendar Queues

## Drawbacks of existing priority queue schemes:

Many scheduling algorithms cannot be realized using fine-grained priority queuing schemes if the computed rank needs to fall within a finite range. eg fair queue, or earliest deadline first (EDF)

## Programmable Calendar Queues (PCQs)

![image-20211026221338708](imgs/image-20211026221338708.png)

Calendar Queue abstraction has a fixed number of buckets or FIFO queues, each of which stores packets scheduled for next N periods.

scheduling algorithms using CQ will do the following:

1. choose a future period from [0, N-1] to enqueue the packet into.
2. periodically decide when a period is over and move onto the next period.
3. when the CQ advances to the next period, the pipeline state has to be suitably modified to ensure the **appropriate computation of ranks for incoming packets**.

Interface methods

1. CQ.enqueue(n): Used by the ingress pipeline to schedule the current packet *n* periods into the future.
2. CQ.dequeue(): Used by the egress pipeline to obtain a buffered packet, if any, for the current period.
3. CQ.rotate(): Used by the pipelines to advance the CQ so that it can start transmitting packets for the next period.

## Programmable Scheduling using PCQs

various scheduling algorithms can be realized using Calendar Queues in conjunction with a pro- grammable packet processing pipeline

### Weighted Fair Queueing

### Earliest Deadline First

### Leaky Bucket Filter

## Implementing PCQs in Hardware

Calendar Queues can be implemented on programmable switches using mutable switch state, multiple FIFO queues, the ability to create and recirculate packets selectively, and the ability to pause/resume queues or alter queue priorities directly in the data plane.

### Implementation overview:

Each *period* in the CQ is mapped to a single FIFO queue within a set of queues associated with the outgoing port

The ingress pipeline computes which *pe- riod* or queue each incoming packet is enqueued into

The queue corresponding to the **current period has the highest priority level**, this queue as the head queue

The queue corresponding to the next period has a lower priority level and is **active/unpaused**. 

### Implementation details:

![image-20211026225624032](imgs/image-20211026225624032.png)

1.  Initiate Rotation

   **When:** initiate rotation when the head queue is empty.

   **How:** check the queue id from which the packet was dequeued to infer whether the head queue is empty

2. Drain queue 

   **when**:  When a rotation begins, we recirculate a special rotate packet to the ingress pipeline so that it stops enqueuing packets in the head queue and begins draining it. and it also ensures that the head queue is completely drained, and no more packets are enqueued into it till the rotation finishes.

   **How: ** the ingress enqueues a special **marker** packet into the head queue **after updating** the head of the calendar queue

3. Finish Rotation

   **when**: **marker** packet is the last packet to be enqueued into the head queue, and its arrival at the egress pipeline means the queue is completely drained.

   **How:**  

   1. The marker packet is recirculated back to the ingress pipeline, and this informs the ingress pipeline that it is safe to reuse the queue for future periods
   2. The ingress changes the priority of the just emptied queue to lowest and also pauses it, essentially pushing the queue to the end of the CQ.

### Analysis 

First, CQs maintain state at the granularity of physical switch queues instead of individual packets or flows.

At any given point in time, there is a designated head queue that is responsible for providing the packets that are to be transmitted.

the rotation operation involves changing just the metadata of queue and that too of at most three queues. This combination of factors allows us to bolt-on the PCQ abstraction on to a traditional TM.

## Extensions

![image-20211027141118965](imgs/image-20211027141118965.png)

# Evaluation

evaluate the practical feasibility, expressiveness, and per- formance of Calendar Queues by implementing them on a **programmable Barefoot Tofino switch** and realizing two clas- sical scheduling algorithms using CQs.

![image-20211027141908456](imgs/image-20211027141908456.png)

![image-20211027141923029](imgs/image-20211027141923029.png)

![image-20211027142006637](imgs/image-20211027142006637.png)

![image-20211027142027559](imgs/image-20211027142027559.png)

