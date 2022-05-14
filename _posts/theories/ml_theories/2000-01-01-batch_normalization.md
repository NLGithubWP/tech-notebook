---
title: batch normalization
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [machine learning basic]
---

# Batch Normalization

## Why need it

if one data sample has multiple features and each feature has a different range, 1-10, 1-1000. Then the loss function is not fair. 

有的w变动对loss影响大，有的对loss影响小。 那么train 过程不容易收敛， w1和w2 需要不同的learning rate。lr设置不好，难收敛

如果范围一样，那么训练就容易收敛了，每个w都根据learning rate 做同样的变动。

![Ho]({{ site.baseurl }}/img/paper-img/image-20220427203226002.png)

### Feature scaling技术

把数据集中的每个 feature dimension 做 normalization， 变成 mean=0， var=1的分布。

Deep-learning 每层的输出都是下一层的输入，所有可以做 feature scaling

## How to do it.

对每一个mini batch， 每一层的输出。不同样本输出的同一个维度都做batch norm。

例如： 有3个example在一个batch 中，每个输出都做batch norm，为了配合激活函数，还可在通过 gemma， beta在做一次变换。

![image-20220427204339574]({{ site.baseurl }}/img/paper-img/image-20220427204339574.png)

Test阶段，没有mini batch ，无法算minibatch， 所以需要记录训练阶段的mean 和sigma。 test时候直接用

![image-20220427204725685]({{ site.baseurl }}/img/paper-img/image-20220427204725685.png)

## Batch norm的好处

1. 因为现在每个w变化都差不多，可以把learning 设置大，训练变快

2. 没有了梯度和梯度爆炸的问题

   输入激活函数前，矩阵的值都变成mean=0的附近，sigmod函数斜率比较大的地方，就不容易有梯度消失这个问题。

3. 对参数的initialization 影响比较小

   ![image-20220427205259701]({{ site.baseurl }}/img/paper-img/image-20220427205259701.png)

4. 不太需要regularization了。 可以对抗overfitting。

## 结构

![image-20220427210222544]({{ site.baseurl }}/img/paper-img/image-20220427210222544.png)