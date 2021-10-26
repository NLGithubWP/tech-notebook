Introduction to modern network load balancing and proxying

# Load balancing and proxying

Load balancing improves the distribution of workloads across multiple computing resources, 

It aims to 

1. **maximize throughput, minimize response time, and avoid overload of any single resource.**
2. provides name abstraction, Fault tolerance, cost and performacne benefits. 

Load balancing usually involves dedicated software or hardware, such as a **multilayer switch** or a **Domain Name System server process**.

**Responsible:**

1. Service discovery: knows all backend addresses. 
2. Health checking: knows which backend is available
3. Load balancing: distribute the workload more uniformly.
4. Persistent per connection:

# Design

When discussing load balancing across the industry today, solutions are often bucketed into two categories: **L4 (Transfer Layer) and L7 (Application Layer)**

 **L4 (Transfer Layer)** 

![image-20211026154015438](imgs/image-20211026154015438.png)

**L4 Limitations:**

For each client, it connect to LB and LB connect to a backend server.

After the connection is estiblished, the client seems only talk to one backend server. 

Under such situation, the imbalance of request rate between different clients could cause the imbalance of workload of corresponding backend servers. 

This defeats the purpose of load balancing where the load is required to balanced distributed across servers. The problem can be fixed by L7 load balancer. 

**L7 (Application Layer)**

![image-20211026162514401](imgs/image-20211026162514401.png)









