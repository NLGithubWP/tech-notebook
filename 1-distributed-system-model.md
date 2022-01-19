# CAP theorem

The CAP theorem says that you can only have two of the three desirable properties of: 

​		C: Consistency, which we can think of as serializability for this discussion; 

​		A: **100% availability**, for both reads and updates; 

​		P: tolerance to network partitions. 

This leads to three kinds of systems: CA, CP and AP, based on what letter you leave out. Note that you are not entitled to 2 of 3, and many systems have zero or one of the properties

# Linearizability 

Focus on **single-operation, single-object,** real-time order

Linearizability is a guarantee about single operations on single objects. It provides a **real-time (i.e., wall-clock) guarantee** on the behavior of **a set of single operations** (often reads and writes) on a single object (e.g., distributed register or data item).

# Serializability

Focus on **multi-operation, multi-object, arbitrary total order**

*Serializability is a guarantee about transactions, or groups of one or more operations over one or more objects.* It guarantees that the **execution of a set of transactions (usually containing read and write operations) over multiple items is equivalent to some serial execution (total ordering) of the transactions.**

Unlike linearizability, serializability does not—by itself—impose any real-time constraints on the ordering of transactions. Serializability is also not composable. Serializability does not imply any kind of deterministic order—it simply requires that ***some* equivalent serial execution exists**

# strict serializability ( = external consistency?)

Combining serializability and linearizability yields *strict serializability*: **transaction behavior is equivalent to some serial execution, and the serial order corresponds to real time**. 

For example, say I begin and commit transaction T1, which writes to item *x*, and you later begin and commit transaction T2, which reads from *x*. **A database providing strict serializability for these transactions will place T1 before T2 in the serial ordering, and T2 will read T1’s write.** **A database providing serializability (but not strict serializability) could order T2 before T1**

As [Herlihy and Wing](http://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf) note, “linearizability can be viewed as a special case of strict serializability where transactions are restricted to **consist of a single operation** applied to a single object.”









