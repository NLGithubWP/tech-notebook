---
title: regularization
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [machine learning basic]
---

# Regularization

![image-20220512212914872]({{ site.baseurl }}/img/paper-img/image-20220512212914872.png)

q 代表正则化程度，q = q 是 l1 正则 （Lasso）， q=2 是 l2 正则 （Ridge）。

**在所有特征中只有少数特征起重要作用的情况下，选择Lasso比较合适，因为它能自动选择特征。而如果所有特征中，大部分特征都能起作用，而且起的作用很平均，那么使用Ridge也许更合适。**

最小化以上方程 = 最小化左边  + 最小化右边。 

分别对左右2个方程画图求解， 交点则是所有可取的解。

可以看到，有了正则化后，交点更容易出现在  w1 = 0 或者 w2 = 0 的位置，这个时候相当于 drop-out 的概念，一些feature的输出置0。



![image-20220512213234157]({{ site.baseurl }}/img/paper-img/image-20220512213234157.png)

![image-20220512213253528]({{ site.baseurl }}/img/paper-img/image-20220512213253528.png)