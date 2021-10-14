# CAP theorem

The CAP theorem says that you can only have two of the three desirable properties of: 

​		C: Consistency, which we can think of as serializability for this discussion; 

​		A: **100% availability**, for both reads and updates; 

​		P: tolerance to network partitions. 

This leads to three kinds of systems: CA, CP and AP, based on what letter you leave out. Note that you are not entitled to 2 of 3, and many systems have zero or one of the properties

# Linearizability 

Focus on **single-operation, single-object,** real-time order

Linearizability is a guarantee about single operations on single objects. It provides a real-time (i.e., wall-clock) guarantee on the behavior of **a set of single operations** (often reads and writes) on a single object (e.g., distributed register or data item).

# Serializability

Focus on **multi-operation, multi-object, arbitrary total order**

*Serializability is a guarantee about transactions, or groups of one or more operations over one or more objects.* It guarantees that the **execution of a set of transactions (usually containing read and write operations) over multiple items is equivalent to *some* serial execution (total ordering) of the transactions.**

Unlike linearizability, serializability does not—by itself—impose any real-time constraints on the ordering of transactions. Serializability is also not composable. Serializability does not imply any kind of deterministic order—it simply requires that ***some* equivalent serial execution exists**





