*Cool*: a COhort OnLine analytical processing system

# Abstract && introduction

A cohort analysis is about comparing the behavior between dif- ferent groups of users, and the grouping is done either based on events or the time users start a service.

Current problems:

1. Traditional OLAP have not been designed to support cohort query. eg, MonetDB is slow to run such cohort query. 

2. redundant storage consumption and transformation cost can be easily incurred once the processors for the two queries have incompatible input/output format and resort to different storage layouts.

Contribution: