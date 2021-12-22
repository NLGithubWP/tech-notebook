Privacy Preserving Vertical Federated Learning for Tree-based Models

# Abstract & Introduction

# Preliminaries

# Solution Overview

# Basic Protocol

If only use MPC to convert private datasets and labels into secretly shared data, and train the model by secure computations, it incurs high communication complexity because it involves O(nd) secretly shared values and most secure computations are communication intensive.

If only use TPHE, it does not support some operations (e.g., comparison)

So, we design our basic protocol using a hybrid framework of TPHE and MPC for vertical tree training. The basic idea is that each client executes as many local computations (e.g., computing split statistics) as possible with the help of TPHE and uses MPC only **when TPHE is insufficient (e.g., deciding the best split).**










