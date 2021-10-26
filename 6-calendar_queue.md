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



### Implementation details:

![image-20211026225624032](imgs/image-20211026225624032.png)

1.  Initiate Rotation

   

2. 





# Evaluation







