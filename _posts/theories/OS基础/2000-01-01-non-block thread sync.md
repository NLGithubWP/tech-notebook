---
title: non-blocking thread synchronization
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [operation system]
---

non-blocking thread synchronization

# Introduction

From [wiki](https://en.wikipedia.org/wiki/Non-blocking_algorithm)

## Motivation

The traditional approach to multi-threaded programming is to use [locks](https://en.wikipedia.org/wiki/Lock_(computer_science)) to synchronize access to shared [resources](https://en.wikipedia.org/wiki/Resource_(computer_science)). Synchronization primitives such as [mutexes](https://en.wikipedia.org/wiki/Mutual_exclusion), [semaphores](https://en.wikipedia.org/wiki/Semaphore_(programming)), and [critical sections](https://en.wikipedia.org/wiki/Critical_section) are all mechanisms by which a programmer can ensure that certain sections of code do not execute concurrently if doing so would corrupt shared memory structures. If one thread attempts to acquire a lock that is already held by another thread, the thread will block until the lock is free.

Other problems are less obvious. For example, certain interactions between locks can lead to error conditions such as [deadlock](https://en.wikipedia.org/wiki/Deadlock), [livelock](https://en.wikipedia.org/wiki/Livelock), and [priority inversion](https://en.wikipedia.org/wiki/Priority_inversion).

Using locks also involves a trade-off between 

1. coarse-grained locking, which can significantly reduce opportunities for [parallelism](https://en.wikipedia.org/wiki/Parallel_computing) 
2. fine-grained locking, which requires more careful design, increases locking overhead and is more prone to bugs.

non-blocking algorithms do not suffer from these downsides, and in addition, are safe for use in [interrupt handlers](https://en.wikipedia.org/wiki/Interrupt_handler)

1. even though the [preempted](https://en.wikipedia.org/wiki/Pre-emptive_multitasking) thread cannot be resumed, progress is still possible without it.
2. In contrast, global data structures protected by mutual exclusion cannot safely be accessed in an interrupt handler, as the preempted thread may be the one holding the lock—but this can be rectified easily by masking the interrupt request during the critical section.

A lock-free data structure can be used to improve performance. A lock-free data structure increases the amount of time spent in parallel execution rather than serial execution, improving performance on a [multi-core processor](https://en.wikipedia.org/wiki/Multi-core_processor), because access to the shared data structure does not need to be serialized to stay coherent.

## Implementation

With few exceptions, non-blocking algorithms use [atomic](https://en.wikipedia.org/wiki/Linearizability) [read-modify-write](https://en.wikipedia.org/wiki/Read-modify-write) primitives that the hardware must provide, the most notable of which is [compare and swap (CAS)](https://en.wikipedia.org/wiki/Compare-and-swap). [Critical sections](https://en.wikipedia.org/wiki/Critical_section) are almost always implemented using standard interfaces over these primitives (in the general case, critical sections will be blocked, even when implemented with these primitives). In the 1990s all non-blocking algorithms had to be written "natively" with the underlying primitives to achieve acceptable performance. However, the emerging field of [software transactional memory](https://en.wikipedia.org/wiki/Software_transactional_memory) promises standard abstractions for writing efficient non-blocking code.

1. Using atomic primitives
2. Using non-blocking data structure without atomic primitives. 
   - a single-reader single-writer [ring buffer](https://en.wikipedia.org/wiki/Circular_buffer) [FIFO](https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)), with a size that evenly divides the overflow of one of the available unsigned integer types, can unconditionally be [implemented safely](https://en.wikipedia.org/wiki/Producer–consumer_problem#Without_semaphores_or_monitors) using only a [memory barrier](https://en.wikipedia.org/wiki/Memory_barrier)
   - [Read-copy-update](https://en.wikipedia.org/wiki/Read-copy-update) with a single writer and any number of readers. (The readers are wait-free; the writer is usually lock-free until it needs to reclaim memory).
   - Read-copy-update with multiple writers and any number of readers. (The readers are wait-free; multiple writers generally serialize with a lock and are not obstruction-free).

Optimizing compiler and CPUs often re-arrange operations, In c++ we can use atomic to tell the compiler not to re-arrange such instructions. and to insert the appropriate memory barriers. 

# 内存屏障

程序在运行时内存实际的访问顺序和程序代码编写的访问顺序不一定一致，这就是内存乱序访问。内存乱序访问行为出现的理由是为了提升程序运行时的性能。内存乱序访问主要发生在两个阶段：

1. 编译时，编译器优化导致内存乱序访问（指令重排）
2. 运行时，多 CPU 间交互引起内存乱序访问

Memory barrier 能够让 CPU 或编译器在内存访问上有序。一个 Memory barrier 之前的内存访问操作必定先于其之后的完成。Memory barrier 包括两类：

1. 编译器 barrier
2. CPU Memory barrier

![image-20220504114649377](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20220504114649377.png)

# Algorithms

There are two types of [non-blocking thread synchronization](http://en.wikipedia.org/wiki/Non-blocking_synchronization) algorithms - lock-free, and wait-free.

## Lock-free algorithms

Any particular computation can be blocked for some period of time. All CPUs are able to continue performing other computations. 

A given thread might be blocked by other threads in a lock-free system, all CPUs can continue doing other useful work without stalls. Lock-free algorithms increase the overall throughput of a system by occasionally increasing the latency of a particular transaction. Most high-end database systems are based on lock-free algorithms, to varying degrees.

### Implementation

1. completing one's own operation, 
2. assisting an obstructing operation, 
3. aborting an obstructing operation,  
4. waiting



## Wait-free algorithm

By contrast, wait-free algorithms ensure that in addition to all CPUs continuing to do useful work, no computation can ever be blocked by another computation. Wait-free algorithms have stronger guarantees than lock-free algorithms and ensure a high throughput without sacrificing the latency of a particular transaction. They’re also much harder to implement, test, and debug. The [lockless page cache](http://lwn.net/Articles/291826/) patches to the Linux kernel are an example of a wait-free system.

### Implementation

Wait-free algorithms were rare until 2011, both in research and in practice. However, in 2011 Kogan and [Petrank](https://en.wikipedia.org/wiki/Erez_Petrank)[[18\]](https://en.wikipedia.org/wiki/Non-blocking_algorithm#cite_note-wf-queue-18) presented a **wait-free queue building on the [CAS](https://en.wikipedia.org/wiki/Compare-and-swap) primitive**, generally available on common hardware. Their construction expanded the lock-free queue of Michael and Scott,[[19\]](https://en.wikipedia.org/wiki/Non-blocking_algorithm#cite_note-lf-queue-19) which is an efficient queue often used in practice. A follow-up paper by Kogan and Petrank[[20\]](https://en.wikipedia.org/wiki/Non-blocking_algorithm#cite_note-wf-fpsp-20) provided a method for making wait-free algorithms fast and used this method to make the wait-free queue practically as fast as its lock-free counterpart. A subsequent paper by Timnat and Petrank[[21\]](https://en.wikipedia.org/wiki/Non-blocking_algorithm#cite_note-wf-simulation-21) provided an automatic mechanism for generating wait-free data structures from lock-free ones. Thus, wait-free implementations are now available for many data structures.

## Compare

In a situation where a system handles dozens of concurrent transactions and has [soft latency requirements](http://en.wikipedia.org/wiki/Real-time_computing#Hard_and_soft_real-time_systems), lock-free systems are a good compromise between development complexity and high concurrency requirements. A database server for a website is a good candidate for a lock-free design. While any given transaction might block, there are always more transactions to process in the meantime, so the CPUs will never stay idle. The challenge is to build a transaction scheduler that maintains a good mean latency, and a well-bounded standard deviation.

In a scenario where a system has roughly as many concurrent transactions as CPU cores or has hard real-time requirements, the developers need to spend the extra time to build wait-free systems. In these cases blocking a single transaction isn’t acceptable - either because there are no other transactions for the CPUs to handle, minimizing the throughput, or a given transaction needs to complete within a well-defined non-probabilistic time period. Nuclear reactor control software is a good candidate for wait-free systems.

