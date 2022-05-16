---
title: cockroachDB-exp
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [practise]
---
# Restart the whole cluster

## Secure

```bash
ps aux | grep cockroach | awk '{print $2}' | xargs kill -9 
rm -rf my-safe-directory
rm -rf certs
rm -rf node*

mkdir certs my-safe-directory

cockroach cert create-ca \
    --certs-dir=certs \
    --ca-key=my-safe-directory/ca.key

cockroach cert create-node \
    localhost \
    $(hostname) \
    --certs-dir=certs \
    --ca-key=my-safe-directory/ca.key

cockroach cert create-client \
    root \
    --certs-dir=certs \
    --ca-key=my-safe-directory/ca.key


cockroach start \
        --certs-dir=certs \
        --store=node1 \
        --listen-addr=localhost:26257 \
        --http-addr=localhost:8280 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --certs-dir=certs \
        --store=node2 \
        --listen-addr=localhost:26258 \
        --http-addr=localhost:8281 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --certs-dir=certs \
        --store=node3 \
        --listen-addr=localhost:26259 \
        --http-addr=localhost:8282 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --certs-dir=certs \
        --store=node4 \
        --listen-addr=localhost:26260 \
        --http-addr=localhost:8283 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background
cockroach start \
        --certs-dir=certs \
        --store=node5 \
        --listen-addr=localhost:26261 \
        --http-addr=localhost:8284 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach init --certs-dir=certs --host=localhost:26257

ps aux | grep cock
cockroach sql --certs-dir=certs --host=localhost:26257
USE cs5424db;
set search_path to workloadA;
alter user naili with password naili;
```

## Insecure

```sql
cockroach start \
        --insecure \
        --store=node1 \
        --listen-addr=localhost:26257 \
        --http-addr=localhost:8280 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --insecure \
        --store=node2 \
        --listen-addr=localhost:26258 \
        --http-addr=localhost:8281 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --insecure \
        --store=node3 \
        --listen-addr=localhost:26259 \
        --http-addr=localhost:8282 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach start \
        --insecure \
        --store=node4 \
        --listen-addr=localhost:26260 \
        --http-addr=localhost:8283 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background
cockroach start \
        --insecure \
        --store=node5 \
        --listen-addr=localhost:26261 \
        --http-addr=localhost:8284 \
        --join=localhost:26257,localhost:26258,localhost:26259,localhost:26260,localhost:26261 \
        --background

cockroach init --insecure --host=localhost:26257

cockroach sql --insecure --host=localhost:26257

USE cs5424db;
set search_path to workloadA;
alter user naili with password naili;
```



# Create table and import data

## 1. create table, load, create_index (slow)

### Example1

```sql
CREATE TABLE IF NOT EXISTS cs5424db.workloadA.order_ori (
    pid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    O_W_ID INT NOT NULL,
    O_D_ID INT NOT NULL,
    O_ID INT NOT NULL,
    O_C_ID INT NOT NULL,
    O_CARRIER_ID INT,
    O_OL_CNT DECIMAL(2,0) NOT NULL,
    O_ALL_LOCAL DECIMAL(1,0) NOT NULL,
    O_ENTRY_D TIMESTAMPTZ DEFAULT now(),
    FAMILY freqWrite (pid, O_W_ID, O_D_ID, O_ID, O_CARRIER_ID),
    FAMILY freqRead (O_C_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D));

IMPORT INTO cs5424db.workloadA.order_ori (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D) CSV DATA ('http://localhost:3000/opt/project_files/data_files_A/order.csv') WITH delimiter = e',', nullif = 'null';

Time: 8.390s total (execution 8.390s / network 0.000s)

CREATE INDEX ON cs5424db.workloadA.order_ori (o_w_id, o_d_id, o_id, o_carrier_id);
CREATE INDEX ON cs5424db.workloadA.order_ori (o_w_id, o_d_id, o_c_id);
CREATE INDEX ON cs5424db.workloadA.order_ori (o_c_id);
CREATE INDEX ON cs5424db.workloadA.order_ori (o_entry_d);

Time: 9.017s total (execution 9.017s / network 0.000s)
CREATE INDEX
Time: 6.881s total (execution 6.881s / network 0.000s)
CREATE INDEX
Time: 6.905s total (execution 6.905s / network 0.000s)
CREATE INDEX
Time: 6.903s total (execution 6.903s / network 0.000s)

```

### Example2 (3000k)

```sql
CREATE TABLE IF NOT EXISTS cs5424db.workloadA.order_line (
    pid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    OL_W_ID INT NOT NULL,
    OL_D_ID INT NOT NULL,
    OL_O_ID INT NOT NULL,
    OL_NUMBER INT NOT NULL,
    OL_I_ID INT NOT NULL,
    OL_DELIVERY_D TIMESTAMPTZ DEFAULT now(),
    OL_AMOUNT DECIMAL(6,2) NOT NULL,
    OL_SUPPLY_W_ID INT NOT NULL,
    OL_QUANTITY DECIMAL(2,0) NOT NULL,
    OL_DIST_INFO CHAR(24) NOT NULL,
    FAMILY freqRead (OL_I_ID, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO),
    FAMILY freqWrite (pid, ol_w_id, ol_d_id, ol_o_id, ol_number, OL_DELIVERY_D));

IMPORT INTO cs5424db.workloadA.order_line (ol_w_id, ol_d_id, ol_o_id, ol_number, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO) CSV DATA ('http://localhost:3000/opt/project_files/data_files_A/order-line.csv') WITH delimiter = e',', nullif = 'null';

Time: 124.034s total (execution 124.033s / network 0.000s)

CREATE INDEX ON cs5424db.workloadA.order_line (ol_w_id, ol_d_id, ol_o_id, ol_number);

Time: 64.249s total (execution 64.248s / network 0.001s)  
```

## 2. Create table with index, load (quick)

### Example1

```sql
CREATE TABLE IF NOT EXISTS cs5424db.workloadA.order_ori (
    pid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    O_W_ID INT NOT NULL,
    O_D_ID INT NOT NULL,
    O_ID INT NOT NULL,
    O_C_ID INT NOT NULL,
    O_CARRIER_ID INT,
    O_OL_CNT DECIMAL(2,0) NOT NULL,
    O_ALL_LOCAL DECIMAL(1,0) NOT NULL,
    O_ENTRY_D TIMESTAMPTZ DEFAULT now(),
    FAMILY freqWrite (pid, O_W_ID, O_D_ID, O_ID, O_CARRIER_ID),
    FAMILY freqRead (O_C_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D),
    INDEX order_ori_joint_id (o_w_id, o_d_id, o_id, o_carrier_id),
    INDEX order_ori_joint_c_id (o_w_id, o_d_id, o_c_id),
    INDEX order_ori_c_id (o_c_id),
    INDEX order_ori_entry_d (o_entry_d));
    
IMPORT INTO cs5424db.workloadA.order_ori (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D)  CSV DATA ('http://localhost:3000/opt/project_files/data_files_A/order.csv') WITH delimiter = e',', nullif = 'null';

Time: 18.825s total (execution 18.824s / network 0.001s)
```

### Example2 (3000k)

```sql
CREATE TABLE IF NOT EXISTS cs5424db.workloadA.order_line (
    pid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    OL_W_ID INT NOT NULL,
    OL_D_ID INT NOT NULL,
    OL_O_ID INT NOT NULL,
    OL_NUMBER INT NOT NULL,
    OL_I_ID INT NOT NULL,
    OL_DELIVERY_D TIMESTAMPTZ DEFAULT now(),
    OL_AMOUNT DECIMAL(6,2) NOT NULL,
    OL_SUPPLY_W_ID INT NOT NULL,
    OL_QUANTITY DECIMAL(2,0) NOT NULL,
    OL_DIST_INFO CHAR(24) NOT NULL,
    FAMILY freqRead (OL_I_ID, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO),
    FAMILY freqWrite (pid, ol_w_id, ol_d_id, ol_o_id, ol_number, OL_DELIVERY_D),
    INDEX order_line_joint_id (ol_w_id, ol_d_id, ol_o_id, ol_number));

IMPORT INTO cs5424db.workloadA.order_line (ol_w_id, ol_d_id, ol_o_id, ol_number, OL_I_ID, OL_DELIVERY_D, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO)
    CSV DATA ('http://localhost:3000/opt/project_files/data_files_A/order-line.csv')
    WITH delimiter = e',', nullif = 'null';
    
Time: 151.911s total (execution 151.911s / network 0.000s)
```

## 3. Read optimizaiton:

#### Follower read

```sql
SELECT I_PRICE, I_NAME FROM item AS OF SYSTEM TIME follower_read_timestamp() WHERE I_ID in (34981, 77989, 73381, 28351, 40577, 89822, 57015);
  i_price |         i_name
----------+--------------------------
       18 | jeepiwbauliwssommaatpx
       18 | obunnbtllietlfrzgadvsd
       10 | xycrtthwkbhmbhgozvapiiy
       20 | spyboiefrndgosga
       40 | ogthbfvggkgcvfuxdqxrlcv
       19 | jibiftmraebdryisas
       26 | visnhoukbsgiwmxceaxdq
(7 rows)

Time: 4ms
NOTICE: -4.8s: using use of follower reads requires an enterprise license. see https://cockroachlabs.com/pricing?cluster=fd188292-d434-4328-b4a7-f528d02621e1 for details on how to enable enterprise features from current statement time instead
NOTICE: -4.8s: using use of follower reads requires an enterprise license. see https://cockroachlabs.com/pricing?cluster=fd188292-d434-4328-b4a7-f528d02621e1 for details on how to enable enterprise features from current statement time instead
total (execution 3ms / network 0ms)
```

##### Do not use batch select !

if using 

```sql
select * from item where i_id in (10, 10, 4);
```

the result will only have 2 records, and the sequence is not the same as (10,10,4), cause bugs.

if use batch select, should generate a map to map each query result to index.

# Check if use index

## indexs

```sql
warehouse PRIMARY KEY (W_ID)
district PRIMARY KEY (D_W_ID, D_ID)
customer PRIMARY KEY (C_W_ID, C_D_ID, C_ID)
order_ori 
		INDEX order_ori_joint_id (o_w_id, o_d_id, o_id, 								o_carrier_id),
    INDEX order_ori_joint_c_id (o_w_id, o_d_id, o_c_id),
    INDEX order_ori_c_id (o_c_id),
    INDEX order_ori_i_id (o_id),
    INDEX order_ori_entry_d (o_entry_d))
order_line  
		INDEX order_line_joint_id (ol_w_id, ol_d_id, ol_o_id, 	         ol_number),
    INDEX order_line_i_id(ol_i_id),
    INDEX order_line_q(OL_QUANTITY)
```

## 1.payment_transaction

query:

```sql
explain UPDATE warehouse SET W_YTD = W_YTD + 9213.21 WHERE W_ID = 10 RETURNING W_STREET_1, W_STREET_2, W_CITY,
W_STATE, W_ZIP;
                                         info
---------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • update
  │ estimated row count: 1
  │ table: warehouse
  │ set: w_ytd
  │ auto commit
  │
  └── • render
      │ estimated row count: 1
      │
      └── • scan
            estimated row count: 1 (10% of the table; stats collected 59 minutes ago)
            table: warehouse@primary
            spans: [/10 - /10]
            locking strength: for update
(17 rows)

```

```sql
explain UPDATE district SET D_YTD = D_YTD + 9213.21 WHERE D_W_ID = 10 and D_ID = 2 returning D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP;
                                        info
------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • update
  │ estimated row count: 1
  │ table: district
  │ set: d_ytd
  │ auto commit
  │
  └── • render
      │ estimated row count: 1
      │
      └── • scan
            estimated row count: 1 (1.0% of the table; stats collected 1 hour ago)
            table: district@primary
            spans: [/10/2 - /10/2]
            locking strength: for update
(17 rows)
```

```sql
explain UPDATE customer SET C_BALANCE = C_BALANCE - 9213.21, C_YTD_PAYMENT = C_YTD_PAYMENT + 9213.21, C_PAYMENT_CNT = C_PAYMENT_CNT + 1 WHERE C_W_ID = 10 and C_D_ID = 2 and C_ID = 2190 RETURNING C_W_ID, C_D_ID, C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE;
                                         info
--------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • update
  │ estimated row count: 1
  │ table: customer
  │ set: c_balance, c_ytd_payment, c_payment_cnt
  │ auto commit
  │
  └── • render
      │ estimated row count: 1
      │
      └── • scan
            estimated row count: 1 (<0.01% of the table; stats collected 1 hour ago)
            table: customer@primary
            spans: [/10/2/2190 - /10/2/2190]
            locking strength: for update
```

## 2. deliver_transaction

```sql
explain update order_ori set o_carrier_id=10 where o_w_id=8 and o_d_id=1 and o_id=(select MIN(o_id) from order_ori where o_w_id=8 and o_d_id=1 and o_carrier_id is null)  returning o_id, o_c_id;
                                                           info
--------------------------------------------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • root
  │
  ├── • update
  │   │ estimated row count: 967
  │   │ table: order_ori
  │   │ set: o_carrier_id
  │   │ auto commit
  │   │
  │   └── • render
  │       │ estimated row count: 967
  │       │
  │       └── • index join
  │           │ estimated row count: 967
  │           │ table: order_ori@primary
  │           │
  │           └── • filter
  │               │ estimated row count: 967
  │               │ filter: o_id = @S1
  │               │
  │               └── • scan
  │                     estimated row count: 2,902 (0.97% of the table; stats collected 2 hours ago)
  │                     table: order_ori@order_ori_joint_id
  │                     spans: [/8/1 - /8/1]
  │
  └── • subquery
      │ id: @S1
      │ original sql: (SELECT min(o_id) FROM order_ori WHERE ((o_w_id = 8) AND (o_d_id = 1)) AND (o_carrier_id IS NULL))
      │ exec mode: one row
      │
      └── • group (scalar)
          │ estimated row count: 1
          │
          └── • limit
              │ estimated row count: 1
              │ count: 1
              │
              └── • filter
                  │ estimated row count: 552
                  │ filter: o_carrier_id IS NULL
                  │
                  └── • scan
                        estimated row count: 2,902 (0.97% of the table; stats collected 2 hours ago)
                        table: order_ori@order_ori_joint_id
                        spans: [/8/1 - /8/1]
```

```sql
explain update order_line set OL_DELIVERY_D =now() where ol_w_id=8 and ol_d_id=1 and ol_o_id=2124;
                                            info
--------------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • update
  │ table: order_line
  │ set: ol_delivery_d
  │ auto commit
  │
  └── • render
      │ estimated row count: 11
      │
      └── • index join
          │ estimated row count: 11
          │ table: order_line@primary
          │
          └── • scan
                estimated row count: 11 (<0.01% of the table; stats collected 2 hours ago)
                table: order_line@order_line_joint_id
                spans: [/8/1/2124 - /8/1/2124]
                locking strength: for update
```

```sql
update customer set (C_BALANCE, C_DELIVERY_CNT) = ((select sum(ol_amount) from order_line    where (ol_w_id, ol_d_id, ol_o_id) in ((8, 1, 2124)) group by ol_o_id), C_DELIVERY_CNT+1)    where (c_w_id, c_d_id, c_id) in ((8, 1, 2908));
                                                                info
-------------------------------------------------------------------------------------------------------------------------------------
  distribution: local
  vectorized: true

  • root
  │
  ├── • update
  │   │ table: customer
  │   │ set: c_balance, c_delivery_cnt
  │   │ auto commit
  │   │
  │   └── • render
  │       │ estimated row count: 1
  │       │
  │       └── • scan
  │             estimated row count: 1 (<0.01% of the table; stats collected 14 minutes ago)
  │             table: customer@primary
  │             spans: [/8/1/2908 - /8/1/2908]
  │             locking strength: for update
  │
  └── • subquery
      │ id: @S1
      │ original sql: (SELECT sum(ol_amount) FROM order_line WHERE (ol_w_id, ol_d_id, ol_o_id) IN ((8, 1, 2124),) GROUP BY ol_o_id)
      │ exec mode: one row
      │
      └── • group
          │ estimated row count: 1
          │
          └── • index join
              │ estimated row count: 11
              │ table: order_line@primary
              │
              └── • scan
                    estimated row count: 11 (<0.01% of the table; stats collected 2 hours ago)
                    table: order_line@order_line_joint_id
                    spans: [/8/1/2124 - /8/1/2124]
                    locking strength: for update
```

# Local Experiments result compare 

**In experiment, each clinet run 510 tx**

## Time used 1 driver

### deliverTx:  read-update-(many_update) 398

Read history data

update order_ori, and order_line

for loop:

​	update one customer per tx

```sql
required_tx_types is:
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is:
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx_time_range [min-max] is :
{'PaymentTxParams': 
			[0.15614604949951172, 0.6048641204833984], 
'TopBalanceTxParams': 
			[0.002360105514526367, 0.004561901092529297], 
'RelCustomerTxParams': [5.525400161743164, 7.103399991989136], 
'StockLevelTxParams': [0.03463602066040039, 0.19315600395202637], 
'NewOrderTxParams': [0.13823390007019043, 0.7757470607757568], 
'OrderStatusTxParams': [0.006901979446411133, 0.012250185012817383], 
'DeliveryTxParams': [1.6580579280853271, 3.323481798171997], 
'PopItemTxParams': [0.04493594169616699, 0.09347701072692871]}
tx_time middle time is :
  {
'PaymentTxParams': 0.24093103408813477, 'TopBalanceTxParams': 0.0033600330352783203, 'RelCustomerTxParams': 6.219896078109741, 'StockLevelTxParams': 0.0728006362915039, 'NewOrderTxParams': 0.3145883083343506, 'OrderStatusTxParams': 0.009333610534667969, 'DeliveryTxParams': 2.6304752826690674, 
'PopItemTxParams': 0.07317614555358887}
tx_time average time is :
{'PaymentTxParams': 0.2541446222199334, 'TopBalanceTxParams': 0.003398467512691722, 'RelCustomerTxParams': 6.279269456863403, 'StockLevelTxParams': 0.08421063423156738, 'NewOrderTxParams': 0.3346138628517709, 'OrderStatusTxParams': 0.009504692895071847, 'DeliveryTxParams': 2.5965065979263158, 
'PopItemTxParams': 0.07145408580177709}
tx time percentage is :
{'PaymentTxParams': '6.883%', 
'TopBalanceTxParams': '0.028%', 
'RelCustomerTxParams': '7.873%', 
'StockLevelTxParams': '0.485%', 
'NewOrderTxParams': '17.20%', 
'OrderStatusTxParams': '0.033%', 
'DeliveryTxParams': '67.06%', 
'PopItemTxParams': '0.340%'}

total 398.7506670951843 second
```

### deliverTx:  one tx for all 192

```sql
required_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx_time_range [min-max] is : 
{'PaymentTxParams': 
[0.10168194770812988, 0.6656451225280762], 'TopBalanceTxParams': 
[0.0022268295288085938, 0.006327152252197266], 'RelCustomerTxParams': 
[4.946579933166504, 6.067049980163574], 'StockLevelTxParams': 
[0.03118300437927246, 0.18277788162231445], 'NewOrderTxParams': 
[0.11868524551391602, 0.7066841125488281], 'OrderStatusTxParams': 
[0.006595134735107422, 0.011111974716186523], 'DeliveryTxParams': 
[0.37049388885498047, 0.8880870342254639], 'PopItemTxParams': 
[0.032930850982666016, 0.08878898620605469]}
tx_time middle time is : 
{'PaymentTxParams': 0.25545787811279297, 'TopBalanceTxParams': 0.003216981887817383, 'RelCustomerTxParams': 5.915307998657227, 'StockLevelTxParams': 0.0698099136352539, 'NewOrderTxParams': 0.33884310722351074, 'OrderStatusTxParams': 0.007817983627319336, 'DeliveryTxParams': 0.5870859622955322, 
'PopItemTxParams': 0.06890702247619629}
tx_time average time is : 
{'PaymentTxParams': 0.2651287140669646, 'TopBalanceTxParams': 0.003412001273211311, 'RelCustomerTxParams': 5.683387374877929, 'StockLevelTxParams': 0.08120476681253185, 'NewOrderTxParams': 0.3451410630854165, 'OrderStatusTxParams': 0.008171371051243373, 'DeliveryTxParams': 0.5954574080346857, 
'PopItemTxParams': 0.06564034913715563}
tx time percentage is : 
{'PaymentTxParams': '14.85%', 
'TopBalanceTxParams': '0.060%', 
'RelCustomerTxParams': '14.74%', 
'StockLevelTxParams': '0.968%', 
'NewOrderTxParams': '36.70%', 
'OrderStatusTxParams': '0.059%', 
'DeliveryTxParams': '31.81%', 
'PopItemTxParams': '0.646%'}
total time used: 192.78175592422485 second
```

### deliverTx:  update district by district 424

each time update one district

```sql
required_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx num percentages is: 
{'PaymentTxParams': '21.13%', 'TopBalanceTxParams': '6.653%', 'RelCustomerTxParams': '0.978%', 'StockLevelTxParams': '4.500%', 'NewOrderTxParams': '40.11%', 'OrderStatusTxParams': '2.739%', 'DeliveryTxParams': '20.15%', 'PopItemTxParams': '3.718%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': 
[0.1638801097869873, 0.4351170063018799], 'TopBalanceTxParams': 
[0.0026769638061523438, 0.00970768928527832], 'RelCustomerTxParams': 
[4.792587757110596, 6.299859046936035], 'StockLevelTxParams': 
[0.027029752731323242, 0.1608259677886963], 'NewOrderTxParams': 
[0.18164706230163574, 0.791996955871582], 'OrderStatusTxParams': 
[0.007290840148925781, 0.01192331314086914], 'DeliveryTxParams': 
[2.504626512527466, 3.3145275115966797], 
'PopItemTxParams': [0.04175901412963867, 0.09454107284545898]}
tx_time middle time is : 
{'PaymentTxParams': 0.2405691146850586, 'TopBalanceTxParams': 0.00413203239440918, 'RelCustomerTxParams': 5.931691884994507, 'StockLevelTxParams': 0.08571791648864746, 'NewOrderTxParams': 0.33698415756225586, 'OrderStatusTxParams': 0.008859872817993164, 'DeliveryTxParams': 2.8518528938293457, 
'PopItemTxParams': 0.06686806678771973}
tx_time average time is : 
{'PaymentTxParams': 0.25068436949341383, 'TopBalanceTxParams': 0.0041195084066951975, 'RelCustomerTxParams': 5.719853401184082, 'StockLevelTxParams': 0.09208858531454335, 'NewOrderTxParams': 0.3448722804464945, 'OrderStatusTxParams': 0.009128195898873466, 'DeliveryTxParams': 2.8540968640336715, 
'PopItemTxParams': 0.06967170614945262}
tx time percentage is : 
{'PaymentTxParams': '6.380%', 
'TopBalanceTxParams': '0.033%',
'RelCustomerTxParams': '6.739%',
'StockLevelTxParams': '0.499%',
'NewOrderTxParams': '16.66%', 
'OrderStatusTxParams': '0.030%', 
'DeliveryTxParams': '69.27%', 
'PopItemTxParams': '0.311%'}

total time used: 424.33997893333435 second
```

### deliverTx:  read-update_without_lock 187

Read history data

Update all once, but without "select...for update"

```sql
required_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx num percentages is: 
{'PaymentTxParams': '21.13%', 'TopBalanceTxParams': '6.653%', 'RelCustomerTxParams': '0.978%', 'StockLevelTxParams': '4.500%', 'NewOrderTxParams': '40.11%', 'OrderStatusTxParams': '2.739%', 'DeliveryTxParams': '20.15%', 'PopItemTxParams': '3.718%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': 
[0.14400196075439453, 0.48920273780822754], 'TopBalanceTxParams': 
[0.002496004104614258, 0.0046498775482177734], 'RelCustomerTxParams': 
[4.9215099811553955, 9.249538898468018], 'StockLevelTxParams': 
[0.02874588966369629, 0.20659780502319336], 'NewOrderTxParams': 
[0.20825886726379395, 0.666205883026123], 'OrderStatusTxParams': 
[0.0068798065185546875, 0.03983473777770996], 'DeliveryTxParams': 
[0.2555239200592041, 0.8404970169067383], 'PopItemTxParams': 
[0.05224180221557617, 0.1262359619140625]}
tx_time middle time is : 
{'PaymentTxParams': 0.2535707950592041, 'TopBalanceTxParams': 0.0034859180450439453, 'RelCustomerTxParams': 5.377862215042114, 'StockLevelTxParams': 0.11979866027832031, 'NewOrderTxParams': 0.34845900535583496, 'OrderStatusTxParams': 0.009082794189453125, 'DeliveryTxParams': 0.496798038482666, 
'PopItemTxParams': 0.07172989845275879}
tx_time average time is : 
{'PaymentTxParams': 0.2582965824339125, 'TopBalanceTxParams': 0.003438837387982537, 'RelCustomerTxParams': 6.197563028335571, 'StockLevelTxParams': 0.1170436195705248, 'NewOrderTxParams': 0.3538451148242485, 'OrderStatusTxParams': 0.012149214744567871, 'DeliveryTxParams': 0.5005713203578319, 
'PopItemTxParams': 0.07649445533752441}
tx time percentage is : 
{'PaymentTxParams': '14.85%', 'TopBalanceTxParams': '0.062%', 'RelCustomerTxParams': '16.50%', 'StockLevelTxParams': '1.433%', 'NewOrderTxParams': '38.63%', 'OrderStatusTxParams': '0.090%', 'DeliveryTxParams': '27.46%', 'PopItemTxParams': '0.774%'}

total time used: 187.74753832817078 second
```

### deliverTx:  read-update_with_lock 179

Read history data

Update all once, but with "select...for update"

```sql
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx num percentages is: 
{'PaymentTxParams': '21.13%', 'TopBalanceTxParams': '6.653%', 'RelCustomerTxParams': '0.978%', 'StockLevelTxParams': '4.500%', 'NewOrderTxParams': '40.11%', 'OrderStatusTxParams': '2.739%', 'DeliveryTxParams': '20.15%', 'PopItemTxParams': '3.718%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': [0.16335010528564453, 0.5330650806427002], 'TopBalanceTxParams': [0.002318859100341797, 0.00529026985168457], 'RelCustomerTxParams': [5.506866931915283, 7.278794050216675], 'StockLevelTxParams': [0.03537487983703613, 0.20850610733032227], 'NewOrderTxParams': [0.19753527641296387, 0.7181658744812012], 'OrderStatusTxParams': [0.006493091583251953, 0.009817123413085938], 'DeliveryTxParams': [0.19803285598754883, 0.7750327587127686], 'PopItemTxParams': [0.044051170349121094, 0.12542390823364258]}
tx_time middle time is : 
{'PaymentTxParams': 0.24466919898986816, 'TopBalanceTxParams': 0.003422260284423828, 'RelCustomerTxParams': 5.9502809047698975, 'StockLevelTxParams': 0.10446000099182129, 'NewOrderTxParams': 0.316270112991333, 'OrderStatusTxParams': 0.008033990859985352, 'DeliveryTxParams': 0.43521714210510254, 
'PopItemTxParams': 0.06883907318115234}
tx_time average time is : 
{'PaymentTxParams': 0.2591760070235641, 'TopBalanceTxParams': 0.003440604490392348, 'RelCustomerTxParams': 6.153213548660278, 'StockLevelTxParams': 0.10385775566101074, 'NewOrderTxParams': 0.34315277657857757, 'OrderStatusTxParams': 0.008057730538504464, 'DeliveryTxParams': 0.44697901114676764, 'PopItemTxParams': 0.07225551103290759}
tx time percentage is : 
{'PaymentTxParams': '15.60%', 'TopBalanceTxParams': '0.065%', 'RelCustomerTxParams': '17.14%', 'StockLevelTxParams': '1.331%', 'NewOrderTxParams': '39.21%', 'OrderStatusTxParams': '0.062%', 'DeliveryTxParams': '25.66%', 'PopItemTxParams': '0.765%'}
total time used: 179.40479707717896 second
```

### deliverTx:  read-update-(one_update) 193

Read history data

update order_ori, and order_line

update all customer in one tx, before updating, use select...for update

```sql
 required_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
 succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
 tx num percentages is: 
{'PaymentTxParams': '21.13%', 'TopBalanceTxParams': '6.653%', 'RelCustomerTxParams': '0.978%', 'StockLevelTxParams': '4.500%', 'NewOrderTxParams': '40.11%', 'OrderStatusTxParams': '2.739%', 'DeliveryTxParams': '20.15%', 'PopItemTxParams': '3.718%'}
 tx_time_range [min-max] is : 
{'PaymentTxParams': [0.1447598934173584, 0.537243127822876], 'TopBalanceTxParams': [0.0023381710052490234, 0.005206108093261719], 'RelCustomerTxParams': [5.607486009597778, 7.530024766921997], 'StockLevelTxParams': [0.03358817100524902, 0.1651158332824707], 'NewOrderTxParams': [0.1485579013824463, 0.7553520202636719], 'OrderStatusTxParams': [0.006378889083862305, 0.010545015335083008], 'DeliveryTxParams': [0.3908543586730957, 0.8421680927276611], 'PopItemTxParams': [0.042954206466674805, 0.0917959213256836]}
 tx_time middle time is : 
{'PaymentTxParams': 0.2537400722503662, 'TopBalanceTxParams': 0.0033087730407714844, 'RelCustomerTxParams': 5.842335939407349, 'StockLevelTxParams': 0.09751582145690918, 'NewOrderTxParams': 0.3116159439086914, 'OrderStatusTxParams': 0.008274078369140625, 'DeliveryTxParams': 0.5995280742645264, 'PopItemTxParams': 0.06537699699401855}
 tx_time average time is : 
{'PaymentTxParams': 0.258017968248438, 'TopBalanceTxParams': 0.0033919460633221794, 'RelCustomerTxParams': 6.176443719863892, 'StockLevelTxParams': 0.09006326094917629, 'NewOrderTxParams': 0.3300563474980796, 'OrderStatusTxParams': 0.008453130722045898, 'DeliveryTxParams': 0.6105537159928998, 'PopItemTxParams': 0.06746746364392732}
 tx time percentage is : 
{'PaymentTxParams': '14.42%', 'TopBalanceTxParams': '0.059%', 'RelCustomerTxParams': '15.98%', 'StockLevelTxParams': '1.072%', 'NewOrderTxParams': '35.02%', 'OrderStatusTxParams': '0.061%', 'DeliveryTxParams': '32.55%', 'PopItemTxParams': '0.663%'}

total time used: 193.15439701080322 second
```



## Time used 40 driver

### deliverTx:  read-update-(many_update)

Read history data

update order_ori, and order_line

for loop:

​	update one customer per tx

```sql
```



### deliverTx:  one tx for all (retry errored)

```sql
too man error, cannot use
```

### deliverTx:  read-update_without_lock(error and slow)

Instead, "select from customer for update" in payment tx, 

```sql
PaymentTxParams WriteTooOldError, cannot use
```

```sql
required_tx_types is: 
{'NewOrderTxParams': 179, 'DeliveryTxParams': 116, 'StockLevelTxParams': 22, 'PopItemTxParams': 19, 'PaymentTxParams': 106, 'TopBalanceTxParams': 38, 'OrderStatusTxParams': 22, 'RelCustomerTxParams': 9}
succeed_tx_types is: 
{'NewOrderTxParams': 179, 'DeliveryTxParams': 116, 'StockLevelTxParams': 22, 'PopItemTxParams': 19, 'PaymentTxParams': 106, 'TopBalanceTxParams': 38, 'OrderStatusTxParams': 22, 'RelCustomerTxParams': 9}
tx num percentages is: 
{'NewOrderTxParams': '35.02%', 'DeliveryTxParams': '22.70%', 'StockLevelTxParams': '4.305%', 'PopItemTxParams': '3.718%', 'PaymentTxParams': '20.74%', 'TopBalanceTxParams': '7.436%', 'OrderStatusTxParams': '4.305%', 'RelCustomerTxParams': '1.761%'}
tx_time_range [min-max] is : 
{'NewOrderTxParams': [0.4197108745574951, 5.957425117492676], 'DeliveryTxParams': [0.055316925048828125, 6.418521881103516], 'StockLevelTxParams': [0.06302809715270996, 0.5879759788513184], 'PopItemTxParams': [0.14858794212341309, 1.8847870826721191], 'PaymentTxParams': 
[0.3015890121459961, 20.024715185165405], 'TopBalanceTxParams': 
[0.00344085693359375, 0.10422205924987793], 'OrderStatusTxParams': 
[0.018672704696655273, 0.1686418056488037], 'RelCustomerTxParams': 
[35.34037184715271, 58.69182014465332]}
tx_time middle time is : 
{'NewOrderTxParams': 0.8999888896942139, 'DeliveryTxParams': 0.35730886459350586, 'StockLevelTxParams': 0.2606949806213379, 'PopItemTxParams': 0.615419864654541, 'PaymentTxParams': 0.5908610820770264, 'TopBalanceTxParams': 0.01160883903503418, 'OrderStatusTxParams': 0.04464316368103027, 'RelCustomerTxParams': 40.61507296562195}
tx_time average time is : 
{'NewOrderTxParams': 1.360372737799277, 'DeliveryTxParams': 0.9666720094351933, 'StockLevelTxParams': 0.28935195099223743, 'PopItemTxParams': 0.720273030431647, 'PaymentTxParams': 0.9975810410841456, 'TopBalanceTxParams': 0.01786107766000848, 'OrderStatusTxParams': 0.05126926031979648, 'RelCustomerTxParams': 42.653216203053795}
tx time percentage is : 
{'NewOrderTxParams': '23.78%', 'DeliveryTxParams': '10.95%', 'StockLevelTxParams': '0.621%', 'PopItemTxParams': '1.336%', 'PaymentTxParams': '10.32%', 'TopBalanceTxParams': '0.066%', 'OrderStatusTxParams': '0.110%', 'RelCustomerTxParams': '37.49%'}

 total time used: 1023.7773869037628 second
```

### deliverTx:  read-update_with_lock (retry errored)

```sql
too man deliverTx WriteTooOldError, cannot use
```

### deliverTx:  read-update-(one_update) with_lock(slow)

has select for update for deliverTx

```sql
very slow, 10s for each tx average
```

### deliverTx:  read-update-(one_update) without_lock(work)

no select for update for both payment and deliverTx

```
no error
```

fastest client:

```sql
required_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
succeed_tx_types is: 
{'PaymentTxParams': 108, 'TopBalanceTxParams': 34, 'RelCustomerTxParams': 5, 'StockLevelTxParams': 23, 'NewOrderTxParams': 205, 'OrderStatusTxParams': 14, 'DeliveryTxParams': 103, 'PopItemTxParams': 19}
tx num percentages is: 
{'PaymentTxParams': '21.13%', 'TopBalanceTxParams': '6.653%', 'RelCustomerTxParams': '0.978%', 'StockLevelTxParams': '4.500%', 'NewOrderTxParams': '40.11%', 'OrderStatusTxParams': '2.739%', 'DeliveryTxParams': '20.15%', 'PopItemTxParams': '3.718%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': 
[0.29213619232177734, 15.85537838935852], 
'TopBalanceTxParams': 
[0.003929853439331055, 0.17207694053649902], 
'RelCustomerTxParams': 
[22.21111297607422, 47.07701516151428], 'StockLevelTxParams': 
[0.09447598457336426, 0.5418219566345215], 
'NewOrderTxParams': [0.33774304389953613, 4.764082908630371], 
'OrderStatusTxParams': 
[0.015622854232788086, 0.10833883285522461], 'DeliveryTxParams': 
[0.04577994346618652, 3.471543073654175], 'PopItemTxParams': 
[0.09161496162414551, 1.0478219985961914]}
tx_time middle time is : 
{'PaymentTxParams': 0.6085801124572754, 'TopBalanceTxParams': 0.012543916702270508, 'RelCustomerTxParams': 31.134135961532593, 'StockLevelTxParams': 0.17986512184143066, 'NewOrderTxParams': 0.9095878601074219, 'OrderStatusTxParams': 0.031976938247680664, 'DeliveryTxParams': 0.21289348602294922, 
'PopItemTxParams': 0.4970381259918213}
tx_time average time is : 
{'PaymentTxParams': 1.1911020014021132, 'TopBalanceTxParams': 0.02088434555951287, 'RelCustomerTxParams': 34.39734263420105, 'StockLevelTxParams': 0.22077977139016855, 'NewOrderTxParams': 1.219485803929771, 'OrderStatusTxParams': 0.03438648155757359, 'DeliveryTxParams': 0.6637284778854222, 
'PopItemTxParams': 0.48234487834729645}
tx time percentage is : 
{'PaymentTxParams': '20.24%', 'TopBalanceTxParams': '0.111%', 'RelCustomerTxParams': '27.06%', 'StockLevelTxParams': '0.799%', 'NewOrderTxParams': '39.34%', 'OrderStatusTxParams': '0.075%', 'DeliveryTxParams': '10.76%', 'PopItemTxParams': '1.442%'}

total time used: 635.3489217758179 second 
```

Slowest client:

```sql
required_tx_types is: 
{'PaymentTxParams': 102, 'OrderStatusTxParams': 23, 'NewOrderTxParams': 216, 'TopBalanceTxParams': 25, 'DeliveryTxParams': 95, 'PopItemTxParams': 21, 'StockLevelTxParams': 18, 'RelCustomerTxParams': 11}
succeed_tx_types is: 
{'PaymentTxParams': 102, 'OrderStatusTxParams': 23, 'NewOrderTxParams': 216, 'TopBalanceTxParams': 25, 'DeliveryTxParams': 95, 'PopItemTxParams': 21, 'StockLevelTxParams': 18, 'RelCustomerTxParams': 11}
tx num percentages is: 
{'PaymentTxParams': '19.96%', 'OrderStatusTxParams': '4.500%', 'NewOrderTxParams': '42.27%', 'TopBalanceTxParams': '4.892%', 'DeliveryTxParams': '18.59%', 'PopItemTxParams': '4.109%', 'StockLevelTxParams': '3.522%', 'RelCustomerTxParams': '2.152%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': 
[0.1857740879058838, 11.892062902450562], 'OrderStatusTxParams': 
[0.0062808990478515625, 0.0505368709564209], 
'NewOrderTxParams': [0.2558581829071045, 18.89508295059204], 
'TopBalanceTxParams': [0.0025110244750976562, 0.17515301704406738], 
'DeliveryTxParams': [0.022066831588745117, 3.8239736557006836], 'PopItemTxParams': [0.04205584526062012, 1.3377859592437744], 'StockLevelTxParams': 
[0.03157401084899902, 0.18178391456604004], 
'RelCustomerTxParams': 
[9.832619905471802, 365.1875970363617]}
tx_time middle time is : 
{'PaymentTxParams': 0.43971800804138184, 'OrderStatusTxParams': 0.013875961303710938, 'NewOrderTxParams': 2.0473878383636475, 'TopBalanceTxParams': 0.0064849853515625, 'DeliveryTxParams': 0.1167299747467041, 
'PopItemTxParams': 0.0714111328125, 
'StockLevelTxParams': 0.08517193794250488, 'RelCustomerTxParams': 14.988978147506714}
tx_time average time is : 
{'PaymentTxParams': 0.8911464074078728, 'OrderStatusTxParams': 0.019917218581489895, 'NewOrderTxParams': 5.707572164358916, 'TopBalanceTxParams': 0.022745304107666016, 'DeliveryTxParams': 0.4815199701409591, 
'PopItemTxParams': 0.18543669155665807, 'StockLevelTxParams': 0.09041327900356716, 'RelCustomerTxParams': 55.98292777755044}
tx time percentage is : 
{'PaymentTxParams': '4.562%', 'OrderStatusTxParams': '0.022%', 'NewOrderTxParams': '61.88%', 'TopBalanceTxParams': '0.028%', 'DeliveryTxParams': '2.296%', 'PopItemTxParams': '0.195%', 'StockLevelTxParams': '0.081%', 'RelCustomerTxParams': '30.91%'}

total time used: 1992.2072050571442 second

```

## Time used 10 driver (read 1200 files each)

### WorkloadB experiments 

#### Original workloadB

```sql
```

#### Use WorkloadA's table and SQLs to run WorkloadB's FIles

Fastest

```sql
required_tx_types is: 
{'StockLevelTxParams': 131, 'PaymentTxParams': 53, 'TopBalanceTxParams': 276, 'RelCustomerTxParams': 235, 'OrderStatusTxParams': 109, 'PopItemTxParams': 245, 'NewOrderTxParams': 96, 'DeliveryTxParams': 59}
succeed_tx_types is: 
{'StockLevelTxParams': 131, 'PaymentTxParams': 53, 'TopBalanceTxParams': 276, 'RelCustomerTxParams': 235, 'OrderStatusTxParams': 109, 'PopItemTxParams': 242, 'NewOrderTxParams': 96, 'DeliveryTxParams': 59}
tx num percentages is: 
{'StockLevelTxParams': '10.90%', 'PaymentTxParams': '4.412%', 'TopBalanceTxParams': '22.98%', 'RelCustomerTxParams': '19.56%', 'OrderStatusTxParams': '9.075%', 'PopItemTxParams': '20.14%', 'NewOrderTxParams': '7.993%', 'DeliveryTxParams': '4.912%'}
tx_time_range [min-max] is : 
{'StockLevelTxParams': [0.021309852600097656, 0.780346155166626], 
'PaymentTxParams': [0.3503396511077881, 9.374873161315918], 
'TopBalanceTxParams': [0.004379749298095703, 6.7614569664001465], 
'RelCustomerTxParams': [0.026685237884521484, 0.971534013748169], 
'OrderStatusTxParams': [0.035845041275024414, 0.5444281101226807], 
'PopItemTxParams': [0.05905580520629883, 1.5464611053466797], 
'NewOrderTxParams': [0.8881630897521973, 24.495393991470337], 
'DeliveryTxParams': [0.9807653427124023, 3.7280821800231934]}
tx_time middle time is : 
{'StockLevelTxParams': 0.17966103553771973, 'PaymentTxParams': 0.6332340240478516, 'TopBalanceTxParams': 0.09718871116638184, 'RelCustomerTxParams': 0.23813700675964355, 'OrderStatusTxParams': 0.10187959671020508, 'PopItemTxParams': 0.3590378761291504, 'NewOrderTxParams': 8.739710092544556, 'DeliveryTxParams': 1.682279109954834}
tx_time average time is : 
{'StockLevelTxParams': 0.22809107795016456, 'PaymentTxParams': 0.8253535144733932, 'TopBalanceTxParams': 0.1481037735939026, 'RelCustomerTxParams': 0.25536085798385294, 'OrderStatusTxParams': 0.13727305788512623, 'PopItemTxParams': 0.3941050787602574, 'NewOrderTxParams': 9.937843697766462, 'DeliveryTxParams': 1.7898441128811593}
tx time percentage is : 
{'StockLevelTxParams': '2.101%', 
'PaymentTxParams': '3.076%', 
'TopBalanceTxParams': '2.875%', 
'RelCustomerTxParams': '4.220%', 
'OrderStatusTxParams': '1.052%', 
'PopItemTxParams': '6.707%', 
'NewOrderTxParams': '67.10%', 
'DeliveryTxParams': '7.427%'}
total time used: 1421.7876341342926 second
```

slowest

```sql
required_tx_types is: 
{'OrderStatusTxParams': 130, 'NewOrderTxParams': 136, 'PopItemTxParams': 228, 'RelCustomerTxParams': 221, 'TopBalanceTxParams': 244, 'DeliveryTxParams': 69, 'StockLevelTxParams': 123, 'PaymentTxParams': 58}
succeed_tx_types is: 
{'OrderStatusTxParams': 130, 'NewOrderTxParams': 136, 'PopItemTxParams': 220, 'RelCustomerTxParams': 221, 'TopBalanceTxParams': 244, 'DeliveryTxParams': 69, 'StockLevelTxParams': 123, 'PaymentTxParams': 58}
tx num percentages is: 
{'OrderStatusTxParams': '10.82%', 'NewOrderTxParams': '11.32%', 'PopItemTxParams': '18.31%', 'RelCustomerTxParams': '18.40%', 'TopBalanceTxParams': '20.31%', 'DeliveryTxParams': '5.745%', 'StockLevelTxParams': '10.24%', 'PaymentTxParams': '4.829%'}
tx_time_range [min-max] is : 
{'OrderStatusTxParams': [0.010293006896972656, 0.9475047588348389], 
'NewOrderTxParams': [0.4942600727081299, 25.753175020217896], 
'PopItemTxParams': [0.06631588935852051, 1.0153987407684326], 
'RelCustomerTxParams': [0.04372715950012207, 0.7704319953918457], 
'TopBalanceTxParams': [0.003039836883544922, 1.1942729949951172], 
'DeliveryTxParams': [0.8192739486694336, 12.131079196929932], 
'StockLevelTxParams': [0.04195284843444824, 1.8515450954437256], 
'PaymentTxParams': [0.3079490661621094, 1.1520459651947021]}
tx_time middle time is : 
{'OrderStatusTxParams': 0.10607695579528809, 'NewOrderTxParams': 7.81226110458374, 'PopItemTxParams': 0.386444091796875, 'RelCustomerTxParams': 0.24327993392944336, 'TopBalanceTxParams': 0.10209298133850098, 'DeliveryTxParams': 1.8284311294555664, 'StockLevelTxParams': 0.21391725540161133, 'PaymentTxParams': 0.6548361778259277}
tx_time average time is : 
{'OrderStatusTxParams': 0.1405129469358004, 'NewOrderTxParams': 9.252860297175015, 'PopItemTxParams': 0.41195380145853217, 'RelCustomerTxParams': 0.25808596179496107, 'TopBalanceTxParams': 0.126881869112859, 'DeliveryTxParams': 2.08274341320646, 'StockLevelTxParams': 0.24644212412640332, 'PaymentTxParams': 0.656815845390846}
tx time percentage is : 
{'OrderStatusTxParams': '1.029%', 
'NewOrderTxParams': '70.92%',
'PopItemTxParams': '5.108%',
'RelCustomerTxParams': '3.214%', 
'TopBalanceTxParams': '1.744%', 
'DeliveryTxParams': '8.099%', 
'StockLevelTxParams': '1.708%',
'PaymentTxParams': '2.147%'}

total time used: 1774.2491250038147 second
```



# Server Experiments result compare 

## Time used 1 driver

### deliverTx: read-update-(many_update)

run 20k txs

```sql
{'PaymentTxParams': 4000, 'OrderStatusTxParams': 800, 'NewOrderTxParams': 8000, 'TopBalanceTxParams': 1200, 'DeliveryTxParams': 4000, 'PopItemTxParams': 800, 'StockLevelTxParams': 800, 'RelCustomerTxParams': 400}
succeed_tx_types is: 
{'PaymentTxParams': 4000, 'OrderStatusTxParams': 800, 'NewOrderTxParams': 8000, 'TopBalanceTxParams': 1200, 'DeliveryTxParams': 4000, 'PopItemTxParams': 800, 'StockLevelTxParams': 800, 'RelCustomerTxParams': 400}
tx num percentages is: 
{'PaymentTxParams': '20.0%', 'OrderStatusTxParams': '4.0%', 'NewOrderTxParams': '40.0%', 'TopBalanceTxParams': '6.0%', 'DeliveryTxParams': '20.0%', 'PopItemTxParams': '4.0%', 'StockLevelTxParams': '4.0%', 'RelCustomerTxParams': '2.0%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': [0.0060214996337890625, 0.33780407905578613], 'OrderStatusTxParams': [0.00596165657043457, 0.07077956199645996], 'NewOrderTxParams': [0.019092321395874023, 0.41755151748657227], 'TopBalanceTxParams': [0.001986265182495117, 0.05776381492614746], 'DeliveryTxParams': [0.07428097724914551, 2.526358127593994], 'PopItemTxParams': [0.04240083694458008, 0.3215057849884033], 'StockLevelTxParams': [0.013997316360473633, 0.3110795021057129], 'RelCustomerTxParams': [6.7307353019714355, 14.297910928726196]}
tx_time middle time is : 
{'PaymentTxParams': 0.008313655853271484, 'OrderStatusTxParams': 0.01041102409362793, 'NewOrderTxParams': 0.043710947036743164, 'TopBalanceTxParams': 0.003559112548828125, 'DeliveryTxParams': 0.10626363754272461, 
'PopItemTxParams': 0.07685685157775879, 'StockLevelTxParams': 0.03121018409729004, 'RelCustomerTxParams': 7.194573163986206}
tx_time average time is : 
{'PaymentTxParams': 0.013122805178165435, 'OrderStatusTxParams': 0.010978831052780151, 'NewOrderTxParams': 0.04540513017773628, 'TopBalanceTxParams': 0.003740751345952352, 'DeliveryTxParams': 0.1465474825501442, 
'PopItemTxParams': 0.07841011106967927, 
'StockLevelTxParams': 0.03239279538393021, 'RelCustomerTxParams': 7.285398296713829}
tx time percentage is : 
{'PaymentTxParams': '1.305%', 'OrderStatusTxParams': '0.218%', 'NewOrderTxParams': '9.032%', 'TopBalanceTxParams': '0.111%', 'DeliveryTxParams': '14.57%', 'PopItemTxParams': '1.559%', 'StockLevelTxParams': '0.644%', 'RelCustomerTxParams': '72.46%'}

total time used: 4021.6916489601135 second
```

### deliverTx:  read-update-(one_update) 

```
```

## Time used 40 driver

### deliverTx:  read-update-(one_update) 

#### each client run 510 txs. 

slowest:

```sql
 required_tx_types is: 
{'DeliveryTxParams': 120, 'PaymentTxParams': 105, 'RelCustomerTxParams': 15, 'PopItemTxParams': 25, 'NewOrderTxParams': 186, 'TopBalanceTxParams': 27, 'OrderStatusTxParams': 18, 'StockLevelTxParams': 15}
 succeed_tx_types is: 
{'DeliveryTxParams': 120, 'PaymentTxParams': 105, 'RelCustomerTxParams': 15, 'PopItemTxParams': 25, 'NewOrderTxParams': 186, 'TopBalanceTxParams': 27, 'OrderStatusTxParams': 18, 'StockLevelTxParams': 15}
 tx num percentages is: 
{'DeliveryTxParams': '23.48%', 'PaymentTxParams': '20.54%', 'RelCustomerTxParams': '2.935%', 'PopItemTxParams': '4.892%', 'NewOrderTxParams': '36.39%', 'TopBalanceTxParams': '5.283%', 'OrderStatusTxParams': '3.522%', 'StockLevelTxParams': '2.935%'}
 tx_time_range [min-max] is : 
{'DeliveryTxParams': [0.07926630973815918, 1.514117956161499], 'PaymentTxParams': [0.00802922248840332, 11.034536123275757], 'RelCustomerTxParams': [4.427427530288696, 30.756058931350708], 'PopItemTxParams': [0.05641460418701172, 1.858823299407959], 'NewOrderTxParams': [0.022408008575439453, 20.853935956954956], 'TopBalanceTxParams': [0.003503561019897461, 0.04083895683288574], 'OrderStatusTxParams': [0.008797883987426758, 0.04307365417480469], 'StockLevelTxParams': [0.028501272201538086, 0.20843172073364258]}
 tx_time middle time is : 
{'DeliveryTxParams': 0.3175313472747803, 'PaymentTxParams': 0.02445507049560547, 'RelCustomerTxParams': 12.067098140716553, 'PopItemTxParams': 0.30762481689453125, 'NewOrderTxParams': 0.12956476211547852, 'TopBalanceTxParams': 0.007569074630737305, 'OrderStatusTxParams': 0.017569541931152344, 'StockLevelTxParams': 0.08283782005310059}
 tx_time average time is : 
{'DeliveryTxParams': 0.3624229967594147, 'PaymentTxParams': 0.15619589941842216, 'RelCustomerTxParams': 13.626139831542968, 'PopItemTxParams': 0.5214762687683105, 'NewOrderTxParams': 1.4489447942344091, 'TopBalanceTxParams': 0.010478673157868561, 'OrderStatusTxParams': 0.021184523900349934, 'StockLevelTxParams': 0.08491495450337729}
 tx time percentage is : 
{'DeliveryTxParams': '7.923%', 'PaymentTxParams': '2.987%', 'RelCustomerTxParams': '37.23%', 'PopItemTxParams': '2.375%', 'NewOrderTxParams': '49.10%', 'TopBalanceTxParams': '0.051%', 'OrderStatusTxParams': '0.069%', 'StockLevelTxParams': '0.232%'}

total time used: 548.8836703300476 second

```

fastes:

```sql
required_tx_types is: 
{'OrderStatusTxParams': 22, 'PopItemTxParams': 24, 'TopBalanceTxParams': 22, 'NewOrderTxParams': 219, 'PaymentTxParams': 103, 'DeliveryTxParams': 94, 'StockLevelTxParams': 18, 'RelCustomerTxParams': 9}
succeed_tx_types is: 
{'OrderStatusTxParams': 22, 'PopItemTxParams': 24, 'TopBalanceTxParams': 22, 'NewOrderTxParams': 219, 'PaymentTxParams': 103, 'DeliveryTxParams': 94, 'StockLevelTxParams': 18, 'RelCustomerTxParams': 9}
tx num percentages is: 
{'OrderStatusTxParams': '4.305%', 'PopItemTxParams': '4.696%', 'TopBalanceTxParams': '4.305%', 'NewOrderTxParams': '42.85%', 'PaymentTxParams': '20.15%', 'DeliveryTxParams': '18.39%', 'StockLevelTxParams': '3.522%', 'RelCustomerTxParams': '1.761%'}
tx_time_range [min-max] is : 
{'OrderStatusTxParams': [0.007178783416748047, 0.05989813804626465], 'PopItemTxParams': [0.04727935791015625, 0.9008371829986572], 'TopBalanceTxParams': [0.0030879974365234375, 0.008611679077148438], 'NewOrderTxParams': [0.019912004470825195, 8.040390253067017], 'PaymentTxParams': [0.006520986557006836, 0.23597025871276855], 'DeliveryTxParams': [0.06527543067932129, 0.8222713470458984], 'StockLevelTxParams': [0.02312159538269043, 0.5057394504547119], 'RelCustomerTxParams': [7.1410744190216064, 33.241151094436646]}
tx_time middle time is : 
{'OrderStatusTxParams': 0.012470006942749023, 'PopItemTxParams': 0.1013646125793457, 'TopBalanceTxParams': 0.003969907760620117, 'NewOrderTxParams': 0.0829315185546875, 'PaymentTxParams': 0.010275602340698242, 'DeliveryTxParams': 0.12951278686523438, 'StockLevelTxParams': 0.11683320999145508, 'RelCustomerTxParams': 16.39730429649353}
tx_time average time is : 
{'OrderStatusTxParams': 0.02321205355904319, 'PopItemTxParams': 0.2693961759408315, 'TopBalanceTxParams': 0.004769942977211692, 'NewOrderTxParams': 0.47296000180179126, 'PaymentTxParams': 0.02685007771242012, 'DeliveryTxParams': 0.2327144551784434, 'StockLevelTxParams': 0.1290303866068522, 'RelCustomerTxParams': 16.89860553211636}
tx time percentage is : 
{'OrderStatusTxParams': '0.176%', 'PopItemTxParams': '2.230%', 'TopBalanceTxParams': '0.036%', 'NewOrderTxParams': '35.74%', 'PaymentTxParams': '0.954%', 'DeliveryTxParams': '7.548%', 'StockLevelTxParams': '0.801%', 'RelCustomerTxParams': '52.47%'}

total time used: 289.8033001422882 second
```

#### each client run 20k txs 

fastest

```sql
required_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
succeed_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
tx num percentages is: 
{'DeliveryTxParams': '20.0%', 'PaymentTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%', 'OrderStatusTxParams': '4.0%', 'RelCustomerTxParams': '2.0%', 'StockLevelTxParams': '4.0%'}
tx_time_range [min-max] is : 
{'DeliveryTxParams': [0.06705665588378906, 4.134788751602173], 
'PaymentTxParams': [0.008793115615844727, 2.2578651905059814], 
'NewOrderTxParams': [0.028956174850463867, 4.808155059814453], 
'PopItemTxParams': [0.09809541702270508, 1.8398656845092773], 
'TopBalanceTxParams': [0.002482891082763672, 0.08717966079711914], 
'OrderStatusTxParams': [0.009213685989379883, 0.15114474296569824], 
'RelCustomerTxParams': [11.96610689163208, 740.4848074913025], 
'StockLevelTxParams': [0.04797101020812988, 6.0720438957214355]}
tx_time middle time is : 
{'DeliveryTxParams': 0.3852264881134033, 'PaymentTxParams': 0.02516651153564453, 'NewOrderTxParams': 0.09827184677124023, 'PopItemTxParams': 0.4055604934692383, 'TopBalanceTxParams': 0.012500286102294922, 'OrderStatusTxParams': 0.030287981033325195, 'RelCustomerTxParams': 37.30942368507385, 'StockLevelTxParams': 0.12674474716186523}
tx_time average time is : 
{'DeliveryTxParams': 0.38580606019496916, 'PaymentTxParams': 0.03734551215171814, 'NewOrderTxParams': 0.11287899878621101, 'PopItemTxParams': 0.42698204576969145, 'TopBalanceTxParams': 0.016467877825101215, 'OrderStatusTxParams': 0.034810789823532105, 'RelCustomerTxParams': 41.62702798485756, 'StockLevelTxParams': 0.14673392564058305}
tx time percentage is : 
{'DeliveryTxParams': '7.811%', 'PaymentTxParams': '0.756%', 'NewOrderTxParams': '4.570%', 'PopItemTxParams': '1.728%', 'TopBalanceTxParams': '0.100%', 'OrderStatusTxParams': '0.140%', 'RelCustomerTxParams': '84.27%', 'StockLevelTxParams': '0.594%'}

total time used: 19756.858887195587 second
```

**other**

```sql
required_tx_types is: 
{'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'DeliveryTxParams': 4000, 'RelCustomerTxParams': 400, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800}
succeed_tx_types is: 
{'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'DeliveryTxParams': 4000, 'RelCustomerTxParams': 400, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800}
tx num percentages is: 
{'PaymentTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'DeliveryTxParams': '20.0%', 'RelCustomerTxParams': '2.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%', 'OrderStatusTxParams': '4.0%', 'StockLevelTxParams': '4.0%'}
tx_time_range [min-max] is : 
{'PaymentTxParams': [0.011700868606567383, 6.021044492721558], 'NewOrderTxParams': [0.03783273696899414, 7.171971321105957], 'DeliveryTxParams': [0.07146692276000977, 3.0683438777923584], 'RelCustomerTxParams': [11.694919347763062, 641.523820400238], 'PopItemTxParams': [0.07011723518371582, 3.489598035812378], 'TopBalanceTxParams': [0.004237651824951172, 0.16576862335205078], 'OrderStatusTxParams': [0.012814521789550781, 0.27407145500183105], 'StockLevelTxParams': [0.0487818717956543, 1.0220296382904053]}
tx_time middle time is : 
{'PaymentTxParams': 0.031154155731201172, 'NewOrderTxParams': 0.17205357551574707, 'DeliveryTxParams': 0.43343448638916016, 'RelCustomerTxParams': 37.826860666275024, 'PopItemTxParams': 0.43820905685424805, 'TopBalanceTxParams': 0.01496434211730957, 'OrderStatusTxParams': 0.03958630561828613, 'StockLevelTxParams': 0.13144588470458984}
tx_time average time is : 
{'PaymentTxParams': 0.044870021760463716, 'NewOrderTxParams': 0.19872215965390205, 'DeliveryTxParams': 0.4211420692801476, 'RelCustomerTxParams': 42.37313334107399, 'PopItemTxParams': 0.4614541020989418, 'TopBalanceTxParams': 0.019939674933751424, 'OrderStatusTxParams': 0.044618663191795346, 'StockLevelTxParams': 0.14893208026885987}
tx time percentage is : 
{'PaymentTxParams': '0.856%', 'NewOrderTxParams': '7.586%', 'DeliveryTxParams': '8.038%', 'RelCustomerTxParams': '80.88%', 'PopItemTxParams': '1.761%', 'TopBalanceTxParams': '0.114%', 'OrderStatusTxParams': '0.170%', 'StockLevelTxParams': '0.568%'}


total time used: 20955.921887159348 second
```



### deliverTx:  read-update-(one_update) +new RelCustomer

#### each client run 20k txs 

Fastest

```sql
required_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
succeed_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
tx num percentages is: 
{'DeliveryTxParams': '20.0%', 'PaymentTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%', 'OrderStatusTxParams': '4.0%', 'RelCustomerTxParams': '2.0%', 'StockLevelTxParams': '4.0%'}
tx_time_range [min-max] is : 
{'DeliveryTxParams': [0.06620430946350098, 6.688509464263916], 
'PaymentTxParams': [0.009000539779663086, 2.7680041790008545], 
'NewOrderTxParams': [0.024884939193725586, 1.7298657894134521], 
'PopItemTxParams': [0.049005746841430664, 0.5829017162322998], 
'TopBalanceTxParams': [0.00313568115234375, 0.1050264835357666], 
'OrderStatusTxParams': [0.006682872772216797, 0.1332716941833496], 
'RelCustomerTxParams': [0.02277207374572754, 36.79711151123047], 
'StockLevelTxParams': [0.021960735321044922, 0.49773216247558594]}
tx_time middle time is : 
{'DeliveryTxParams': 0.39609622955322266, 
'PaymentTxParams': 0.03075861930847168, 
'NewOrderTxParams': 0.10427308082580566, 
'PopItemTxParams': 0.19124054908752441, 
'TopBalanceTxParams': 0.0076677799224853516, 
'OrderStatusTxParams': 0.015861988067626953, 
'RelCustomerTxParams': 0.10349750518798828, 
'StockLevelTxParams': 0.06265783309936523}
tx_time average time is : 
{'DeliveryTxParams': 0.7029072520136833,
'PaymentTxParams': 0.06172101533412933, 
'NewOrderTxParams': 0.13628420701622962, 
'PopItemTxParams': 0.1981538102030754, 
'TopBalanceTxParams': 0.010825100739796957, 
'OrderStatusTxParams': 0.02111440360546112, 
'RelCustomerTxParams': 0.6241337299346924, 
'StockLevelTxParams': 0.07460264593362809}
tx time percentage is : 
{'DeliveryTxParams': '60.46%', 'PaymentTxParams': '5.309%', 'NewOrderTxParams': '23.44%', 'PopItemTxParams': '3.409%', 'TopBalanceTxParams': '0.279%', 'OrderStatusTxParams': '0.363%', 'RelCustomerTxParams': '5.368%', 'StockLevelTxParams': '1.283%'}

total time used: 4649.980607509613 second 
```

Slowest 

```sql
required_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'StockLevelTxParams': 800, 'RelCustomerTxParams': 400, 'OrderStatusTxParams': 800, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200}
succeed_tx_types is: 
{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'StockLevelTxParams': 800, 'RelCustomerTxParams': 400, 'OrderStatusTxParams': 800, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200}
tx num percentages is: 
{'DeliveryTxParams': '20.0%', 'PaymentTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'StockLevelTxParams': '4.0%', 'RelCustomerTxParams': '2.0%', 'OrderStatusTxParams': '4.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%'}
tx_time_range [min-max] is : 
{'DeliveryTxParams': [0.06003117561340332, 6.687764644622803], 'PaymentTxParams': [0.008917570114135742, 3.1278812885284424], 'NewOrderTxParams': [0.02373361587524414, 3.4845988750457764], 'StockLevelTxParams': [0.02218031883239746, 0.4671635627746582], 'RelCustomerTxParams': [0.031206130981445312, 456.23539090156555], 'OrderStatusTxParams': [0.00858449935913086, 0.11835384368896484], 'PopItemTxParams': [0.05227994918823242, 3.2975709438323975], 'TopBalanceTxParams': [0.0033254623413085938, 0.11398196220397949]}
tx_time middle time is : 
{'DeliveryTxParams': 0.3909952640533447, 'PaymentTxParams': 0.027904987335205078, 'NewOrderTxParams': 0.22519445419311523, 'StockLevelTxParams': 0.06427168846130371, 'RelCustomerTxParams': 0.12715625762939453, 'OrderStatusTxParams': 0.019356966018676758, 'PopItemTxParams': 0.16162490844726562, 'TopBalanceTxParams': 0.008049726486206055}
tx_time average time is : 
{'DeliveryTxParams': 0.5571800107359887, 'PaymentTxParams': 0.053697246849536896, 'NewOrderTxParams': 0.3464160120487213, 'StockLevelTxParams': 0.07861154049634933, 'RelCustomerTxParams': 4.050478057861328, 'OrderStatusTxParams': 0.025514654219150543, 'PopItemTxParams': 0.18711606055498123, 'TopBalanceTxParams': 0.013249912858009338}
tx time percentage is : 
{'DeliveryTxParams': '31.42%', 'PaymentTxParams': '3.028%', 'NewOrderTxParams': '39.07%', 'StockLevelTxParams': '0.886%', 'RelCustomerTxParams': '22.84%', 'OrderStatusTxParams': '0.287%', 'PopItemTxParams': '2.110%', 'TopBalanceTxParams': '0.224%'}

total time used: 7091.655424118042 second
```

### WorkloadB experiments

#### Original workloadB-without history read

fatest

```sql
required_tx_types is: 
{'PopItemTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'RelCustomerTxParams': 4000, 'TopBalanceTxParams': 4000, 'NewOrderTxParams': 2000, 'DeliveryTxParams': 1000}
succeed_tx_types is: 
{'PopItemTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'RelCustomerTxParams': 4000, 'TopBalanceTxParams': 4000, 'NewOrderTxParams': 2000, 'DeliveryTxParams': 1000}
tx num percentages is: 
{'PopItemTxParams': '20.0%', 'OrderStatusTxParams': '10.0%', 'PaymentTxParams': '5.0%', 'StockLevelTxParams': '10.0%', 'RelCustomerTxParams': '20.0%', 'TopBalanceTxParams': '20.0%', 'NewOrderTxParams': '10.0%', 'DeliveryTxParams': '5.0%'}
tx_time_range [min-max] is : 
{'PopItemTxParams': [0.043653011322021484, 2.937039852142334], 'OrderStatusTxParams': [0.006611824035644531, 0.10404109954833984], 'PaymentTxParams': [0.007398128509521484, 4.316748857498169], 'StockLevelTxParams': [0.022179365158081055, 2.0832979679107666], 'RelCustomerTxParams': [0.01425313949584961, 27.941823959350586], 
'TopBalanceTxParams': [0.0034437179565429688, 0.30124664306640625], 
'NewOrderTxParams': [0.03072643280029297, 6.985389232635498], 'DeliveryTxParams': [0.10069131851196289, 0.9532630443572998]}
tx_time middle time is : 
{'PopItemTxParams': 0.15568161010742188, 'OrderStatusTxParams': 0.013590812683105469, 'PaymentTxParams': 0.012779712677001953, 'StockLevelTxParams': 0.07341122627258301, 'RelCustomerTxParams': 0.15813660621643066, 'TopBalanceTxParams': 0.006154298782348633, 'NewOrderTxParams': 1.3094377517700195, 'DeliveryTxParams': 0.19967222213745117}
tx_time average time is : 
{'PopItemTxParams': 0.1743237208724022, 'OrderStatusTxParams': 0.01665512478351593, 'PaymentTxParams': 0.050359912872314457, 'StockLevelTxParams': 0.08441155648231506, 'RelCustomerTxParams': 0.21077250862121583, 'TopBalanceTxParams': 0.009081676185131072, 'NewOrderTxParams': 1.4749051374197006, 'DeliveryTxParams': 0.21938607478141783}
tx time percentage is : 
{'PopItemTxParams': '13.94%', 'OrderStatusTxParams': '0.666%', 'PaymentTxParams': '1.006%', 'StockLevelTxParams': '3.375%', 'RelCustomerTxParams': '16.85%', 'TopBalanceTxParams': '0.726%', 
'NewOrderTxParams': '58.98%', 'DeliveryTxParams': '4.386%'}
```

Slowest

```sql
required_tx_types is: 
{'DeliveryTxParams': 1000, 'TopBalanceTxParams': 4000, 'PopItemTxParams': 4000, 'RelCustomerTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'NewOrderTxParams': 2000}
succeed_tx_types is: 
{'DeliveryTxParams': 1000, 'TopBalanceTxParams': 4000, 'PopItemTxParams': 4000, 'RelCustomerTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'NewOrderTxParams': 2000}
tx num percentages is: 
{'DeliveryTxParams': '5.0%', 'TopBalanceTxParams': '20.0%', 'PopItemTxParams': '20.0%', 'RelCustomerTxParams': '20.0%', 'OrderStatusTxParams': '10.0%', 'PaymentTxParams': '5.0%', 'StockLevelTxParams': '10.0%', 'NewOrderTxParams': '10.0%'}
tx_time_range [min-max] is : 
{'DeliveryTxParams': [0.12121295928955078, 2.440812110900879], 
'TopBalanceTxParams': [0.003799915313720703, 0.0838615894317627], 
'PopItemTxParams': [0.0406031608581543, 2.9131178855895996], 
'RelCustomerTxParams': [0.02302241325378418, 59.59907388687134], 
'OrderStatusTxParams': [0.008373022079467773, 0.22054052352905273], 
'PaymentTxParams': [0.010132074356079102, 3.7663419246673584], 
'StockLevelTxParams': [0.020366191864013672, 1.4866340160369873], 
'NewOrderTxParams': [0.038144826889038086, 6.873712778091431]}
tx_time middle time is : 
{'DeliveryTxParams': 0.2431316375732422, 'TopBalanceTxParams': 0.009315967559814453, 'PopItemTxParams': 0.1574840545654297, 'RelCustomerTxParams': 0.36730384826660156, 'OrderStatusTxParams': 0.019392967224121094, 'PaymentTxParams': 0.024661779403686523, 'StockLevelTxParams': 0.0724327564239502, 'NewOrderTxParams': 1.283696174621582}
tx_time average time is : 
{'DeliveryTxParams': 0.2744468514919281, 'TopBalanceTxParams': 0.012445117533206939, 'PopItemTxParams': 0.1759404569864273, 'RelCustomerTxParams': 0.4861455803513527, 'OrderStatusTxParams': 0.02346905255317688, 'PaymentTxParams': 0.08069565296173095, 'StockLevelTxParams': 0.08723806083202362, 'NewOrderTxParams': 1.4893892135620117}
tx time percentage is : 
{'DeliveryTxParams': '4.385%', 'TopBalanceTxParams': '0.795%', 'PopItemTxParams': '11.24%', 'RelCustomerTxParams': '31.07%', 'OrderStatusTxParams': '0.750%', 'PaymentTxParams': '1.289%', 'StockLevelTxParams': '2.788%', 'NewOrderTxParams': '47.60%'}
```

#### Original workloadB-with history read

fastest

```sql
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'TopBalanceTxParams': 4000, 'OrderStatusTxParams': 2000, 'RelCustomerTxParams': 4000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000, 'DeliveryTxParams': 1000}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'TopBalanceTxParams': 4000, 'OrderStatusTxParams': 2000, 'RelCustomerTxParams': 4000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000, 'DeliveryTxParams': 1000}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'PopItemTxParams': '20.0%', 'PaymentTxParams': '5.0%', 'TopBalanceTxParams': '20.0%', 'OrderStatusTxParams': '10.0%', 'RelCustomerTxParams': '20.0%', 'NewOrderTxParams': '10.0%', 'StockLevelTxParams': '10.0%', 'DeliveryTxParams': '5.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{
'PopItemTxParams': [0.04119515419006348, 2.123006582260132], 
'PaymentTxParams': [0.008533000946044922, 2.292015790939331], 
'TopBalanceTxParams': [0.002079010009765625, 0.022124767303466797], 
'OrderStatusTxParams': [0.006811380386352539, 0.2652583122253418], 
'RelCustomerTxParams': [0.018296003341674805, 34.09693646430969], 
'NewOrderTxParams': [0.03715825080871582, 25.316109657287598], 
'StockLevelTxParams': [0.020386695861816406, 3.5080161094665527], 
'DeliveryTxParams': [0.0776679515838623, 4.463620185852051]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'PopItemTxParams': 0.10662221908569336, 'PaymentTxParams': 0.013123750686645508, 'TopBalanceTxParams': 0.003186464309692383, 'OrderStatusTxParams': 0.012742042541503906, 'RelCustomerTxParams': 0.1964890956878662, 'NewOrderTxParams': 1.231938362121582, 'StockLevelTxParams': 0.048102617263793945, 'DeliveryTxParams': 0.17396807670593262}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{
'PopItemTxParams': 0.11312417471408844, 
'PaymentTxParams': 0.059289373874664306, 
'TopBalanceTxParams': 0.003660040080547333, 
'OrderStatusTxParams': 0.015427935361862183, 
'RelCustomerTxParams': 0.2941498779058456,
'NewOrderTxParams': 1.3363996965885163,
'StockLevelTxParams': 0.061666582942008975, 
'DeliveryTxParams': 0.19275231623649597}
tx time percentage is : {
'PopItemTxParams': '9.570%', 
'PaymentTxParams': '1.254%', 
'TopBalanceTxParams': '0.309%', 
'OrderStatusTxParams': '0.652%', 
'RelCustomerTxParams': '24.88%', 
'NewOrderTxParams': '56.53%', 
'StockLevelTxParams': '2.608%', 
'DeliveryTxParams': '4.076%'}

total time used: 4727.852853536606 second =====================
```

notes:

in new order, this is very slow

```sql
DEBUG:__main__:[UPDATE district SET D_NEXT_O_ID = D_NEXT_O_ID + 1 WHERE D_W_ID = 1 and D_ID = 2 returning D_NEXT_O_ID, d_tax;]:   25216425 us
```

In relatedCustomer , this is very slow

```sql
SELECT IP_I1_ID, IP_I2_ID FROM item_pair WHERE IP_W_ID = 1 AND IP_D_ID = 1 AND IP_C_ID = 1250 ]:   141559 us
```

Slowest

```sql
NFO:__main__:connect to postgresql://naili:@xcnd56:27257/cs5424db, Read file /home/stuproj/cs4224p/temp/tasks/project_files_4/xact_files_B/21.txt and run workload B

required_tx_types is: 
INFO:__main__:{'OrderStatusTxParams': 2000, 'TopBalanceTxParams': 4000, 'DeliveryTxParams': 1000, 'RelCustomerTxParams': 4000, 'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'OrderStatusTxParams': 2000, 'TopBalanceTxParams': 4000, 'DeliveryTxParams': 1000, 'RelCustomerTxParams': 4000, 'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'OrderStatusTxParams': '10.0%', 'TopBalanceTxParams': '20.0%', 'DeliveryTxParams': '5.0%', 'RelCustomerTxParams': '20.0%', 'PopItemTxParams': '20.0%', 'PaymentTxParams': '5.0%', 'NewOrderTxParams': '10.0%', 'StockLevelTxParams': '10.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'OrderStatusTxParams': [0.006795644760131836, 0.10069489479064941], 'TopBalanceTxParams': [0.003291606903076172, 0.12161922454833984], 'DeliveryTxParams': [0.0820157527923584, 3.863018035888672], 'RelCustomerTxParams': [0.023424148559570312, 227.8955101966858], 'PopItemTxParams': [0.03539538383483887, 0.9753758907318115], 'PaymentTxParams': [0.011014938354492188, 2.0942068099975586], 'NewOrderTxParams': [0.0325620174407959, 20.171861171722412], 'StockLevelTxParams': [0.018865108489990234, 3.837775707244873]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'OrderStatusTxParams': 0.016010046005249023, 'TopBalanceTxParams': 0.006000995635986328, 'DeliveryTxParams': 0.17874932289123535, 'RelCustomerTxParams': 0.32175230979919434, 'PopItemTxParams': 0.10468935966491699, 'PaymentTxParams': 0.020900964736938477, 'NewOrderTxParams': 0.8674423694610596, 'StockLevelTxParams': 0.04611515998840332}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'OrderStatusTxParams': 0.01981469678878784, 'TopBalanceTxParams': 0.007989742159843445, 'DeliveryTxParams': 0.2026522629261017, 'RelCustomerTxParams': 0.6211161369085312, 'PopItemTxParams': 0.11278318470716477, 'PaymentTxParams': 0.04882942843437195, 'NewOrderTxParams': 1.0938691581487656, 'StockLevelTxParams': 0.05847097361087799}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{
'OrderStatusTxParams': '0.711%', 
'TopBalanceTxParams': '0.573%', 
'DeliveryTxParams': '3.639%', 
'RelCustomerTxParams': '44.61%', 
'PopItemTxParams': '8.101%',
'PaymentTxParams': '0.876%', 
'NewOrderTxParams': '39.28%', 
'StockLevelTxParams': '2.100%'}

total time used: 5568.371900320053 second
```

#### Use WorkloadA's table and SQLs to run WorkloadB's FIles (100 tx each client only)

set log-detail to false

read history data

Test only 100 

```sql
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 7, 'TopBalanceTxParams': 21, 'NewOrderTxParams': 11, 'RelCustomerTxParams': 19, 'StockLevelTxParams': 9, 'PopItemTxParams': 17, 'PaymentTxParams': 5, 'OrderStatusTxParams': 12}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 7, 'TopBalanceTxParams': 21, 'NewOrderTxParams': 11, 'RelCustomerTxParams': 19, 'StockLevelTxParams': 9, 'PopItemTxParams': 17, 'PaymentTxParams': 5, 'OrderStatusTxParams': 12}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'DeliveryTxParams': '6.930%', 'TopBalanceTxParams': '20.79%', 'NewOrderTxParams': '10.89%', 'RelCustomerTxParams': '18.81%', 'StockLevelTxParams': '8.910%', 'PopItemTxParams': '16.83%', 'PaymentTxParams': '4.950%', 'OrderStatusTxParams': '11.88%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'DeliveryTxParams': [0.08615255355834961, 1.168724775314331], 'TopBalanceTxParams': [0.0034422874450683594, 0.06905293464660645], 'NewOrderTxParams': [0.10105299949645996, 1.1931192874908447], 'RelCustomerTxParams': [0.05597734451293945, 5.553996562957764], 'StockLevelTxParams': [0.05745959281921387, 2.086024284362793], 'PopItemTxParams': [0.09922575950622559, 1.0295624732971191], 'PaymentTxParams': [0.01640772819519043, 0.08808469772338867], 'OrderStatusTxParams': [0.011550426483154297, 0.12307357788085938]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'DeliveryTxParams': 0.43329501152038574, 'TopBalanceTxParams': 0.0073413848876953125, 'NewOrderTxParams': 0.19635534286499023, 'RelCustomerTxParams': 0.19931316375732422, 'StockLevelTxParams': 0.08235359191894531, 'PopItemTxParams': 0.3723490238189697, 'PaymentTxParams': 0.04191994667053223, 'OrderStatusTxParams': 0.04134869575500488}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'DeliveryTxParams': 0.4667386668069022, 'TopBalanceTxParams': 0.010829891477312361, 'NewOrderTxParams': 0.3025944232940674, 'RelCustomerTxParams': 0.5301264461718107, 'StockLevelTxParams': 0.3165012200673421, 'PopItemTxParams': 0.36663471951204185, 'PaymentTxParams': 0.05115065574645996, 'OrderStatusTxParams': 0.047169347604115806}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'DeliveryTxParams': '12.16%', 'TopBalanceTxParams': '0.847%', 'NewOrderTxParams': '12.39%', 'RelCustomerTxParams': '37.51%', 'StockLevelTxParams': '10.60%', 'PopItemTxParams': '23.21%', 'PaymentTxParams': '0.952%', 'OrderStatusTxParams': '2.108%'}
INFO:__main__:============================ total time used: 26.84976100921631 second =====================
```

slowest

```sql
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'PopItemTxParams': 17, 'RelCustomerTxParams': 21, 'TopBalanceTxParams': 29, 'NewOrderTxParams': 13, 'OrderStatusTxParams': 7, 'StockLevelTxParams': 5, 'PaymentTxParams': 5, 'DeliveryTxParams': 4}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'PopItemTxParams': 17, 'RelCustomerTxParams': 21, 'TopBalanceTxParams': 29, 'NewOrderTxParams': 13, 'OrderStatusTxParams': 7, 'StockLevelTxParams': 5, 'PaymentTxParams': 5, 'DeliveryTxParams': 4}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'PopItemTxParams': '16.83%', 'RelCustomerTxParams': '20.79%', 'TopBalanceTxParams': '28.71%', 'NewOrderTxParams': '12.87%', 'OrderStatusTxParams': '6.930%', 'StockLevelTxParams': '4.950%', 'PaymentTxParams': '4.950%', 'DeliveryTxParams': '3.960%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'PopItemTxParams': [0.051306724548339844, 0.4875149726867676], 'RelCustomerTxParams': [0.027841567993164062, 159.23399114608765], 'TopBalanceTxParams': [0.0019061565399169922, 0.011357784271240234], 'NewOrderTxParams': [0.030652999877929688, 6.566680669784546], 'OrderStatusTxParams': [0.007851362228393555, 0.014297246932983398], 'StockLevelTxParams': [0.027576684951782227, 3.9981250762939453], 'PaymentTxParams': [0.008518695831298828, 0.011621475219726562], 'DeliveryTxParams': [0.07341361045837402, 1.7170028686523438]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'PopItemTxParams': 0.08894801139831543, 'RelCustomerTxParams': 0.08863329887390137, 'TopBalanceTxParams': 0.0023033618927001953, 'NewOrderTxParams': 0.04650449752807617, 'OrderStatusTxParams': 0.008876562118530273, 'StockLevelTxParams': 0.03904247283935547, 'PaymentTxParams': 0.011400461196899414, 'DeliveryTxParams': 0.3067479133605957}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'PopItemTxParams': 0.12733178980210247, 'RelCustomerTxParams': 10.390213955016364, 'TopBalanceTxParams': 0.0027938217952333646, 'NewOrderTxParams': 0.6073061319497916, 'OrderStatusTxParams': 0.010353531156267439, 'StockLevelTxParams': 0.8286996364593506, 'PaymentTxParams': 0.010662078857421875, 'DeliveryTxParams': 0.5964043736457825}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'PopItemTxParams': '0.920%', 'RelCustomerTxParams': '92.81%', 'TopBalanceTxParams': '0.034%', 'NewOrderTxParams': '3.358%', 'OrderStatusTxParams': '0.030%', 'StockLevelTxParams': '1.762%', 'PaymentTxParams': '0.022%', 'DeliveryTxParams': '1.014%'}
INFO:__main__:============================ total time used: 235.0949182510376 second =====================
```



# 优化RelCustomer

## 问题1: 每个order每次select..join时间都一样

```sql
[ SELECT O_ID, O_W_ID, O_D_ID FROM order_ori WHERE O_W_ID = 5 AND O_D_ID = 3 AND O_C_ID = 2289 ]:   1201 us

[ WITH items AS (SELECT OL_I_ID FROM order_line WHERE OL_O_ID = 3011 AND OL_W_ID = 5 AND OL_D_ID = 3), customer_ol AS (SELECT O_C_ID, O_W_ID, O_D_ID, O_ID, order_line.OL_I_ID FROM order_ori JOIN order_line ON O_W_ID = order_line.OL_W_ID AND O_D_ID = order_line.OL_D_ID AND O_ID = order_line.OL_O_ID WHERE O_W_ID <> 5 ) SELECT DISTINCT O_W_ID, O_D_ID, O_C_ID FROM items LEFT JOIN customer_ol ON items.OL_I_ID = customer_ol.OL_I_ID GROUP BY O_C_ID, O_W_ID, O_D_ID, O_ID HAVING COUNT(*) >= 2 ]:   9123286 us

[ WITH items AS (SELECT OL_I_ID FROM order_line WHERE OL_O_ID = 1815 AND OL_W_ID = 5 AND OL_D_ID = 3), customer_ol AS (SELECT O_C_ID, O_W_ID, O_D_ID, O_ID, order_line.OL_I_ID FROM order_ori JOIN order_line ON O_W_ID = order_line.OL_W_ID AND O_D_ID = order_line.OL_D_ID AND O_ID = order_line.OL_O_ID WHERE O_W_ID <> 5 ) SELECT DISTINCT O_W_ID, O_D_ID, O_C_ID FROM items LEFT JOIN customer_ol ON items.OL_I_ID = customer_ol.OL_I_ID GROUP BY O_C_ID, O_W_ID, O_D_ID, O_ID HAVING COUNT(*) >= 2 ]:   8458964 us

```

# Server Experiments final

## check workloadA tables range information

```sql
root@xcnd55:27257/cs5424db> show ranges from table workloadA.customer;
  start_key | end_key | range_id | range_size_mb | lease_holder | lease_holder_locality | replicas | replica_localities
------------+---------+----------+---------------+--------------+-----------------------+----------+---------------------
  NULL      | /1/1    |      458 |             0 |            5 |                       | {2,4,5}  | {,,}
  /1/1      | /1/10   |      462 |     32.160704 |            5 |                       | {2,3,5}  | {,,}
  /1/10     | /2/1    |      397 |       3.57507 |            5 |                       | {2,3,5}  | {,,}
  /2/1      | /2/10   |      373 |     32.127344 |            3 |                       | {2,3,4}  | {,,}
  /2/10     | /3/1    |      376 |      3.553868 |            3 |                       | {2,3,4}  | {,,}
  /3/1      | /3/10   |      437 |     32.216628 |            3 |                       | {2,3,4}  | {,,}
  /3/10     | /4/1    |      438 |      3.572468 |            3 |                       | {2,3,5}  | {,,}
  /4/1      | /4/10   |      439 |     32.129364 |            3 |                       | {1,3,4}  | {,,}
  /4/10     | /5/1    |      440 |      3.583344 |            3 |                       | {2,3,5}  | {,,}
  /5/1      | /5/10   |      441 |     32.129172 |            3 |                       | {2,3,5}  | {,,}
  /5/10     | /6/1    |      442 |      3.571376 |            3 |                       | {2,3,5}  | {,,}
  /6/1      | /6/10   |      445 |     32.191418 |            3 |                       | {1,2,3}  | {,,}
  /6/10     | /7/1    |      446 |      3.564142 |            1 |                       | {1,2,3}  | {,,}
  /7/1      | /7/10   |      477 |     32.180704 |            3 |                       | {1,2,3}  | {,,}
  /7/10     | /8/1    |      398 |       3.57043 |            5 |                       | {2,4,5}  | {,,}
  /8/1      | /8/10   |      399 |     32.107972 |            2 |                       | {2,3,5}  | {,,}
  /8/10     | /9/1    |      400 |      3.553534 |            2 |                       | {2,3,5}  | {,,}
  /9/1      | /9/10   |      401 |     32.091696 |            2 |                       | {2,3,5}  | {,,}
  /9/10     | /10/1   |      402 |      3.570706 |            2 |                       | {2,3,5}  | {,,}
  /10/1     | /10/10  |      403 |     32.118422 |            2 |                       | {2,3,5}  | {,,}
  /10/10    | NULL    |      404 |     14.341556 |            5 |                       | {1,2,5}  | {,,}
```

## worloadA experiment(district is not splited)

fatestest

```sql
INFO:__main__:connect to postgresql://rootuser:@xcnd57:27257/cs5424db, Read file /home/stuproj/cs4224p/temp/tasks/project_files_4/xact_files_A/27.txt and run workload A
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'NewOrderTxParams': 8000, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'RelCustomerTxParams': 400, 'StockLevelTxParams': 800}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'DeliveryTxParams': '20.0%', 'PaymentTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%', 'OrderStatusTxParams': '4.0%', 'RelCustomerTxParams': '2.0%', 'StockLevelTxParams': '4.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{
'DeliveryTxParams': [0.0940394401550293, 18.964545726776123], 
'PaymentTxParams': [0.008363485336303711, 1.4704015254974365], 'NewOrderTxParams': [0.022224903106689453, 6.635453939437866], 'PopItemTxParams': [0.050208330154418945, 0.6432342529296875], 'TopBalanceTxParams': [0.0022013187408447266, 0.15984082221984863], 'OrderStatusTxParams': [0.00648188591003418, 0.05884099006652832], 'RelCustomerTxParams': [0.034255266189575195, 7.857444524765015], 'StockLevelTxParams': [0.020989179611206055, 0.47068023681640625]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'DeliveryTxParams': 0.37264513969421387, 'PaymentTxParams': 0.018275022506713867, 'NewOrderTxParams': 0.07090187072753906, 'PopItemTxParams': 0.1388378143310547, 'TopBalanceTxParams': 0.00434422492980957, 'OrderStatusTxParams': 0.013213634490966797, 'RelCustomerTxParams': 0.1091468334197998, 'StockLevelTxParams': 0.05873537063598633}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'DeliveryTxParams': 0.4993351148366928, 'PaymentTxParams': 0.041156271040439604, 'NewOrderTxParams': 0.10065338760614395, 'PopItemTxParams': 0.15924189507961273, 'TopBalanceTxParams': 0.005224022666613261, 'OrderStatusTxParams': 0.015345950424671174, 'RelCustomerTxParams': 0.20358444035053253, 'StockLevelTxParams': 0.066924666762352}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'DeliveryTxParams': '61.43%', 'PaymentTxParams': '5.063%', 'NewOrderTxParams': '24.76%', 'PopItemTxParams': '3.918%', 'TopBalanceTxParams': '0.192%', 'OrderStatusTxParams': '0.377%', 'RelCustomerTxParams': '2.504%', 'StockLevelTxParams': '1.646%'}
total time used: 3251.0644114017487 second
```

slowest

````sql

````

Cluster information

![image-20211104210601420](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211104210601420.png)

![image-20211104210658298](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211104210658298.png)

![image-20211104210834426](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211104210834426.png)

## workloadA experiment(district is splitted) why this is so slow?/

Fastest

```sql
INFO:__main__:connect to postgresql://rootuser:@xcnd55:27257/cs5424db, Read file /home/stuproj/cs4224p/temp/tasks/project_files_4/xact_files_A/25.txt and run workload A
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'NewOrderTxParams': 8000, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'PaymentTxParams': 4000, 'RelCustomerTxParams': 400}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'NewOrderTxParams': 8000, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800, 'PopItemTxParams': 800, 'TopBalanceTxParams': 1200, 'PaymentTxParams': 4000, 'RelCustomerTxParams': 400}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'DeliveryTxParams': '20.0%', 'NewOrderTxParams': '40.0%', 'OrderStatusTxParams': '4.0%', 'StockLevelTxParams': '4.0%', 'PopItemTxParams': '4.0%', 'TopBalanceTxParams': '6.0%', 'PaymentTxParams': '20.0%', 'RelCustomerTxParams': '2.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'DeliveryTxParams': [0.09678363800048828, 21.767359018325806], 'NewOrderTxParams': [0.024239063262939453, 7.722882270812988], 'OrderStatusTxParams': [0.006879329681396484, 0.21355724334716797], 'StockLevelTxParams': [0.023659944534301758, 1.3360991477966309], 'PopItemTxParams': [0.05456805229187012, 3.062171220779419], 'TopBalanceTxParams': [0.002875089645385742, 0.3323400020599365], 'PaymentTxParams': [0.008802652359008789, 15.16224193572998], 'RelCustomerTxParams': [0.028119802474975586, 10.305521965026855]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'DeliveryTxParams': 0.4503483772277832, 'NewOrderTxParams': 0.08659934997558594, 'OrderStatusTxParams': 0.013454198837280273, 'StockLevelTxParams': 0.05750107765197754, 'PopItemTxParams': 0.15394377708435059, 'TopBalanceTxParams': 0.004498720169067383, 'PaymentTxParams': 0.028304100036621094, 'RelCustomerTxParams': 0.11582589149475098}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'DeliveryTxParams': 0.778711769759655, 'NewOrderTxParams': 0.3065736477971077, 'OrderStatusTxParams': 0.016812161803245546, 'StockLevelTxParams': 0.07329640686511993, 'PopItemTxParams': 0.1976630276441574, 'TopBalanceTxParams': 0.005740454196929931, 'PaymentTxParams': 0.13048452234268187, 'RelCustomerTxParams': 0.2747782760858536}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'DeliveryTxParams': '48.35%', 'NewOrderTxParams': '38.07%', 'OrderStatusTxParams': '0.208%', 'StockLevelTxParams': '0.910%', 'PopItemTxParams': '2.454%', 'TopBalanceTxParams': '0.106%', 'PaymentTxParams': '8.101%', 'RelCustomerTxParams': '1.706%'}
 total time used: 6442.281774759293 second 
```

slowest

```sql
INFO:__main__:connect to postgresql://rootuser:@xcnd55:27257/cs5424db, Read file /home/stuproj/cs4224p/temp/tasks/project_files_4/xact_files_A/35.txt and run workload A
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'RelCustomerTxParams': 400, 'PopItemTxParams': 800, 'NewOrderTxParams': 8000, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'DeliveryTxParams': 4000, 'PaymentTxParams': 4000, 'RelCustomerTxParams': 400, 'PopItemTxParams': 800, 'NewOrderTxParams': 8000, 'TopBalanceTxParams': 1200, 'OrderStatusTxParams': 800, 'StockLevelTxParams': 800}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'DeliveryTxParams': '20.0%', 'PaymentTxParams': '20.0%', 'RelCustomerTxParams': '2.0%', 'PopItemTxParams': '4.0%', 'NewOrderTxParams': '40.0%', 'TopBalanceTxParams': '6.0%', 'OrderStatusTxParams': '4.0%', 'StockLevelTxParams': '4.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'DeliveryTxParams': [0.10470461845397949, 20.285513401031494], 'PaymentTxParams': [0.008340835571289062, 19.08874011039734], 'RelCustomerTxParams': [0.03162956237792969, 168.91484308242798], 'PopItemTxParams': [0.05150938034057617, 1.0880217552185059], 'NewOrderTxParams': [0.026800155639648438, 29.250999450683594], 'TopBalanceTxParams': [0.0022656917572021484, 0.07593226432800293], 'OrderStatusTxParams': [0.007979154586791992, 0.07962322235107422], 'StockLevelTxParams': [0.023247480392456055, 0.7286357879638672]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'DeliveryTxParams': 0.498460054397583, 'PaymentTxParams': 0.02234649658203125, 'RelCustomerTxParams': 0.13301682472229004, 'PopItemTxParams': 0.13823652267456055, 'NewOrderTxParams': 0.25033116340637207, 'TopBalanceTxParams': 0.004361867904663086, 'OrderStatusTxParams': 0.013583898544311523, 'StockLevelTxParams': 0.060243844985961914}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'DeliveryTxParams': 0.7653842960596084, 'PaymentTxParams': 0.09842191231250763, 'RelCustomerTxParams': 1.104385917186737, 'PopItemTxParams': 0.17024195492267608, 'NewOrderTxParams': 0.6707052890062332, 'TopBalanceTxParams': 0.005735321044921875, 'OrderStatusTxParams': 0.016672326028347017, 'StockLevelTxParams': 0.07074818849563598}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'DeliveryTxParams': '32.29%', 'PaymentTxParams': '4.153%', 'RelCustomerTxParams': '4.660%', 'PopItemTxParams': '1.436%', 'NewOrderTxParams': '56.60%', 'TopBalanceTxParams': '0.072%', 'OrderStatusTxParams': '0.140%', 'StockLevelTxParams': '0.597%'}
total time used: 9479.322530269623 second 
```

## check workloadB tables range information

## workloadB experiment(district is splitted)

Fastest

```sql
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'PopItemTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'RelCustomerTxParams': 4000, 'TopBalanceTxParams': 4000, 'NewOrderTxParams': 2000, 'DeliveryTxParams': 1000}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'PopItemTxParams': 4000, 'OrderStatusTxParams': 2000, 'PaymentTxParams': 1000, 'StockLevelTxParams': 2000, 'RelCustomerTxParams': 4000, 'TopBalanceTxParams': 4000, 'NewOrderTxParams': 2000, 'DeliveryTxParams': 1000}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'PopItemTxParams': '20.0%', 'OrderStatusTxParams': '10.0%', 'PaymentTxParams': '5.0%', 'StockLevelTxParams': '10.0%', 'RelCustomerTxParams': '20.0%', 'TopBalanceTxParams': '20.0%', 'NewOrderTxParams': '10.0%', 'DeliveryTxParams': '5.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'PopItemTxParams': [0.029532432556152344, 1.1351370811462402], 'OrderStatusTxParams': [0.005969047546386719, 11.313726663589478], 'PaymentTxParams': [0.007120609283447266, 4.932584524154663], 'StockLevelTxParams': [0.01968860626220703, 0.7491550445556641], 'RelCustomerTxParams': [0.019487619400024414, 39.51293349266052], 'TopBalanceTxParams': [0.002714395523071289, 0.0668337345123291], 'NewOrderTxParams': [0.028239965438842773, 10.329297065734863], 'DeliveryTxParams': [0.08482646942138672, 6.401065826416016]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'PopItemTxParams': 0.09830760955810547, 'OrderStatusTxParams': 0.011962413787841797, 'PaymentTxParams': 0.011313438415527344, 'StockLevelTxParams': 0.04557657241821289, 'RelCustomerTxParams': 0.2080976963043213, 'TopBalanceTxParams': 0.004521608352661133, 'NewOrderTxParams': 0.9234161376953125, 'DeliveryTxParams': 0.15929460525512695}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'PopItemTxParams': 0.10706163960695267, 'OrderStatusTxParams': 0.01982469952106476, 'PaymentTxParams': 0.039915404081344606, 'StockLevelTxParams': 0.056616720080375674, 'RelCustomerTxParams': 0.28210580748319625, 'TopBalanceTxParams': 0.005966431319713593, 'NewOrderTxParams': 1.0354568886756896, 'DeliveryTxParams': 0.18945905900001525}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'PopItemTxParams': '10.60%', 'OrderStatusTxParams': '0.982%', 'PaymentTxParams': '0.988%', 'StockLevelTxParams': '2.804%', 'RelCustomerTxParams': '27.94%', 'TopBalanceTxParams': '0.591%', 'NewOrderTxParams': '51.29%', 'DeliveryTxParams': '4.692%'}
 total time used: 4037.345842599869 second
```

slowest

```sql
INFO:__main__:=======> required_tx_types is: 
INFO:__main__:{'OrderStatusTxParams': 2000, 'TopBalanceTxParams': 4000, 'DeliveryTxParams': 1000, 'RelCustomerTxParams': 4000, 'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000}
INFO:__main__:=======> succeed_tx_types is: 
INFO:__main__:{'OrderStatusTxParams': 2000, 'TopBalanceTxParams': 4000, 'DeliveryTxParams': 1000, 'RelCustomerTxParams': 4000, 'PopItemTxParams': 4000, 'PaymentTxParams': 1000, 'NewOrderTxParams': 2000, 'StockLevelTxParams': 2000}
INFO:__main__:=======> tx num percentages is: 
INFO:__main__:{'OrderStatusTxParams': '10.0%', 'TopBalanceTxParams': '20.0%', 'DeliveryTxParams': '5.0%', 'RelCustomerTxParams': '20.0%', 'PopItemTxParams': '20.0%', 'PaymentTxParams': '5.0%', 'NewOrderTxParams': '10.0%', 'StockLevelTxParams': '10.0%'}
INFO:__main__:=======> tx_time_range [min-max] is : 
INFO:__main__:{'OrderStatusTxParams': [0.0071184635162353516, 0.09766054153442383], 'TopBalanceTxParams': [0.003351449966430664, 0.21988606452941895], 'DeliveryTxParams': [0.10575675964355469, 1.0390677452087402], 'RelCustomerTxParams': [0.02222919464111328, 51.281330585479736], 'PopItemTxParams': [0.037384986877441406, 11.277520179748535], 'PaymentTxParams': [0.010007619857788086, 2.8379220962524414], 'NewOrderTxParams': [0.03411602973937988, 10.52436900138855], 'StockLevelTxParams': [0.01657843589782715, 3.6650354862213135]}
INFO:__main__:=======> tx_time middle time is : 
INFO:__main__:{'OrderStatusTxParams': 0.015763521194458008, 'TopBalanceTxParams': 0.006165504455566406, 'DeliveryTxParams': 0.19103074073791504, 'RelCustomerTxParams': 0.2876155376434326, 'PopItemTxParams': 0.10260510444641113, 'PaymentTxParams': 0.01948404312133789, 'NewOrderTxParams': 0.9821634292602539, 'StockLevelTxParams': 0.04608583450317383}
INFO:__main__:=======> tx_time average time is : 
INFO:__main__:{'OrderStatusTxParams': 0.019520679593086242, 'TopBalanceTxParams': 0.008644869148731232, 'DeliveryTxParams': 0.2155011205673218, 'RelCustomerTxParams': 0.3969092663526535, 'PopItemTxParams': 0.11523041915893555, 'PaymentTxParams': 0.04866554617881775, 'NewOrderTxParams': 1.076444769501686, 'StockLevelTxParams': 0.05775388872623444}
INFO:__main__:=======> tx time percentage is : 
INFO:__main__:{'OrderStatusTxParams': '0.837%', 'TopBalanceTxParams': '0.742%', 'DeliveryTxParams': '4.624%', 'RelCustomerTxParams': '34.07%', 'PopItemTxParams': '9.892%', 'PaymentTxParams': '1.044%', 'NewOrderTxParams': '46.20%', 'StockLevelTxParams': '2.478%'}

total time used: 4659.487995624542 second 
```

## Compare

![image-20211105112236084](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211105112236084.png)

![image-20211105112413638](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211105112413638.png)

![image-20211105112732164](https://github.com/NLGithubWP/tech-notebook/raw/master/img/a_img_store/image-20211105112732164.png)



# Errors and problems

## Slow querys

```sql
// in NewOrder, it takes 17-20s sometimes, in heavy select worklaod
UPDATE district SET D_NEXT_O_ID = D_NEXT_O_ID + 1 WHERE D_W_ID = 1 and D_ID = 2 returning D_NEXT_O_ID, d_tax; 
```

## Set Transaction timestamp cause read

if set transaction timestamp, it's a read only transaction. 

Option1 

```sql
# get current time
cur.execute("SELECT CURRENT_TIMESTAMP;")            cur_times = cur.fetchall()
modified_time = cur_times[0][0] -	   		   datetime.timedelta(minutes=3)
# update time to read historical data
cur.execute("SET TRANSACTION AS OF SYSTEM TIME
            '{}';".format(str(modified_time)))
# check current time
cur.execute("SELECT CURRENT_TIMESTAMP;")
cur_times = cur.fetchall()

```

Option2 

```sql
cur.execute("SET TRANSACTION AS OF SYSTEM TIME '-10s'")
```

Error 

```sql
cannot execute UPDATE in a read-only transaction
```

## Bbort reason Pusher Aborted Error

### Deadlock?

https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer.html

**Deadlock**: Some transaction *B* is trying to acquire conflicting locks in reverse order from transaction *A*.

If there is a deadlock between transactions (i.e., they're each blocked by each other's Write Intents), one of the transactions is randomly aborted. In the above example, this would happen if `TxnA` blocked `TxnB` on `key1` and `TxnB` blocked `TxnA` on `key2`.

**If you are encountering deadlocks**: Avoid producing deadlocks in your application by making sure that transactions acquire locks in the same order.

Sequences:

```sql
new_order_tx: 
	update district
	insert order_ori
	update stock
	insert order_line
payment_tx:
	update district
	update warehouse
	update customer
delivery_tx:
	update order_ori
	update order_line
	update customer
```

## Write-Write conflict?

Write-write conflict: Another [high-priority transaction](https://www.cockroachlabs.com/docs/v21.1/transactions#transaction-priorities) *B* encountered a write intent by our transaction *A*, and tried to push *A*'s timestamp.

Try to set paymentTx to higher priority since it;s has less work to do/ 

## Follower-Read

```sql
using use of follower reads requires an enterprise license. see https://cockroachlabs.com/pricing?cluster=f9c9840d-6db4-46cc-92f4-77586d10c151 for details on how to enable enterprise features from current statement time instead
NOTICE: -4.8s: using use of follower reads requires an enterprise license. see https://cockroachlabs.com/pricing?cluster=f9c9840d-6db4-46cc-92f4-77586d10c151 for details on how to enable enterprise features from current statement time instead
 total (execution 3ms / network 1ms)
```

# Something found

## 读历史数据

```sql
SET TRANSACTION AS OF SYSTEM TIME '-5s'
```

意思是把当前tx的timestamp设置成5秒前的，如果5秒前就已经被其他事务在更新，那么还是会等待。

start(b) - start(a)  > 5 还是读不到，
start(b) - start(a) <5 才可以
所以这个越大，并发读越高, 但是读的越老

## why need manully split?



## update 阻塞select?? default isolation level??



## 一个tx加锁

一个tx 有多条update，遇到update才对该数据加锁，而不是一开始就对本tx所有操作的加锁 **(死锁的来源)**

## 小表leftjoin 大表

左边小表数据很重复多条，匹配右边

## 大表right join小表

和上面的结果一样

## join表缓存？

多次select..join和单次一样

```

```

## IN 用index吗？（why）

有时候用到，有时候用不到。 Why？？？

```sql
explain SELECT OL_W_ID, OL_D_ID, OL_O_ID, OL_I_ID FROM order_line WHERE ol_i_id in (1,2,3,4,6,7,8,9,10);
```

如果在创建表的时候，没建立索引，而是后面在create index，，，就没用到

```sql

```

结论： 用in的时候，索引要在表创建的时候，就创建好，

## Join operations

#### Lookup join:

The [cost-based optimizer](https://www.cockroachlabs.com/docs/v21.1/cost-based-optimizer) decides when it would be beneficial to use a lookup join. 

**Lookup joins are used when there is a large imbalance in size between the two tables, as it only reads the smaller table and then looks up matches in the larger table.** 

A lookup join requires that the right-hand (i.e., larger) table be indexed on the equality column. A [partial index](https://www.cockroachlabs.com/docs/v21.1/partial-indexes) can only be used if it contains the subset of rows being looked up.

Lookup joins are performed on two tables as follows:

1. CockroachDB reads each row in the small table.
2. CockroachDB then scans (or "looks up") the larger table for matches to the smaller table and outputs the matching rows.

```
```

#### Hash Join

If a merge join cannot be used, CockroachDB uses a [hash join](https://en.wikipedia.org/wiki/Hash_join). Hash joins are computationally expensive and require additional memory.

Hash joins are performed on two tables as follows:

1. CockroachDB reads both tables and attempts to pick the smaller table.
2. CockroachDB creates an in-memory [hash table](https://en.wikipedia.org/wiki/Hash_table) on the smaller table. If the hash table is too large, it will spill over to disk storage (which could affect performance).
3. CockroachDB then scans the large table, looking up each row in the hash table.

#### Merge Join

To perform a [merge join](https://en.wikipedia.org/wiki/Sort-merge_join) of two tables, **both tables must be indexed on the equality columns, and any indexes must have the same ordering.** 

Merge joins offer better computational performance and more efficient memory usage than [hash joins](https://www.cockroachlabs.com/docs/stable/joins.html#hash-joins). When tables and indexes are ordered for a merge, CockroachDB chooses to use merge joins over hash joins, by default. When merge conditions are not met, CockroachDB resorts to the slower hash joins. Merge joins can be used only with [distributed query processing](https://www.cockroachlabs.com/blog/local-and-distributed-processing-in-cockroachdb/).

Merge joins are performed on the indexed columns of two tables as follows:

1. CockroachDB checks for indexes on the equality columns and that they are ordered the same (i.e., `ASC` or `DESC`).
2. CockroachDB takes one row from each table and compares them.
   - For inner joins:
     - If the rows are equal, CockroachDB returns the rows.
     - If there are multiple matches, the cartesian product of the matches is returned.
     - If the rows are not equal, CockroachDB discards the lower-value row and repeats the process with the next row until all rows are processed.
   - For outer joins:
     - If the rows are equal, CockroachDB returns the rows.
     - If there are multiple matches, the cartesian product of the matches is returned.
     - If the rows are not equal, CockroachDB returns `NULL` for the non-matching column and repeats the process with the next row until all rows are processed.
