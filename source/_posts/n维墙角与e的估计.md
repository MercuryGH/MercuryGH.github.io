---
title: n维墙角与e的估计
date: 2023-07-10 18:36:44
tags:
- 数学
- 概率论
---
> http://www.matrix67.com/blog/archives/3507
>
> https://www.zhihu.com/question/64089362

记$U_1,U_2,\dots$为一列独立随机变量，均服从$(0,1]$上的均匀分布。记

$$
\xi = \min\{n \geq 1: U_1+U_2+\dots+U_n > 1\},
$$

求$E(\xi)$。

<!--more-->

## 解答

### 方法零：动态规划法

> 本方法出处未知，且似乎并不严谨，但能算出正确的结果，仅供参考

记$f_x$是部分和$U_1 + \dots + U_n$首次超过$x$（$x \in [0, 1]$）的期望项数，则答案在$f_1$。初值条件为$f_0 = 0$。记当前状态为$i$，表示部分和已经达到$i$项，但$U_1 + \dots + U_i < x$。考虑状态从$f_{x-u}, u \in [0, x)$转移得到：

$$
f_x = \int_{0}^x f_{x - u} \, \mathrm d u + 1.
$$

上式可改写成

$$
f_x = \int_0^x f_{u} \, \mathrm du + 1.
$$

解积分方程得到$f_x = \mathrm e^x$。故答案为$\mathrm e$。

### 方法一：墙角积分法

从$(0,1]$中均匀地抽取一个数若干次，直至这些数的和恰好大于$1$为止，题目所求的就是抽取次数的数学期望。抽取次数一定为$2,3,\dots$，我们用原始的想法一个一个检验：

考虑抽取$2$次，但这些数的和仍小于或等于$1$的概率，记为$p_2$，这要求

$$
U_1 + U_2 \leq 1,
$$

由于$U_i \in (0,1])$，故在坐标系中，上述面积占$(0,1] \times (0,1]$的一半。于是$p_2=\frac{1}{2}$。

考虑抽取$3$次，但这些数的和仍小于或等于$1$的概率，记为$p_3$，类似地

$$
U_1 + U_2 + U_3 \leq 1,
$$

由于

$$
\iiint\limits_{U_1 + U_2 + U_3 \leq 1} \mathrm dU_1 \mathrm dU_2 \mathrm dU_3 = \frac{1}{6},
$$

故$p_3 = \frac{1}{6}$。

考虑抽取$n$次，但这些数的和仍小于或等于$1$的概率，记为$p_n$，由归纳法得

$$
\begin{matrix}\underbrace{\int \dots \int}\\\small{n重, \sum_{i=1}^n U_i \leq 1}\end{matrix} \mathrm dU_1\dots \mathrm dU_n = \frac{1}{n!}.
$$

我们求抽取$n$次，这些数的和恰好大于$1$的概率，这意味着抽取$n-1$次时，这些数的和仍小于或等于$1$。即

$$
P = \left(1-\frac{1}{n!} \right) - \left(1-\frac{1}{(n-1)!}\right).
$$

上式可以从“状态转移”的角度理解，即$P(抽取n次和大于1)$可以由$P(抽取n-1次和大于1)$和$P(抽取n-1次和仍然小于或等于1)$转移而来，前者是以概率$1$转移，后者的转移概率不必关心。于是，用$P(抽取n次和大于1)$减去$P(抽取n-1次和大于1)$就能得出我们“从期望的路径转移而来”的结果。

可求得数学期望

$$
E(\xi) = \sum_{n=2}^{\infty} nP = \sum_{n=2}^{\infty} n \frac{n-1}{n!} = \sum_{n=2}^{\infty} \frac{1}{(n-2)!} = \mathrm e.
$$

PS: 本题的结论可以推广到

$$
\xi(x) = \min\{n \geq 1: U_1+U_2+\dots+U_n > x\}, x \in [0, 1],
$$

只需求

$$
\begin{matrix}\underbrace{\int \dots \int}\\\small{n重, \sum_{i=1}^n U_i \leq x}\end{matrix} \mathrm dU_1\dots \mathrm dU_n = \frac{x^n}{n!}.
$$

故

$$
P(\xi(x) > n) = \frac{x^n}{n!}. \tag{*}
$$

特别地，$x=1$时，$P(\xi > n) = \frac{1}{n!}$。我们研究$(*)$式对应的期望，有

$$
\begin{aligned}
EX(x) &= \sum_{n=1}^{\infty}n\left (\left( 1- \frac{x^n}{n!}\right) - \left( 1- \frac{x^{n-1}}{(n-1)!}\right)\right ) \\
&= \sum_{n = 1}^{\infty} \frac{x^{n-1}}{(n-1)!}(n-x) \\
&= \sum_{n=1}^{\infty}\frac{n x^{n-1}}{(n-1)!} - x \sum_{n = 1}^{\infty} \frac{x^{n-1}}{(n-1)!} \\
&= (x+1)\mathrm e^x - x \mathrm e^x \\
&= \mathrm e^x.
\end{aligned}
$$

结果令人意外地简洁。但请注意该结论仅限于$x \in [0, 1]$的情况，$x > 1$的情况更加复杂，详见 https://mathworld.wolfram.com/UniformSumDistribution.html.

#### 变体

将题干所求的随机变量$\xi$改为$\gamma$，定义如下：

$$
\gamma = \min\{n \geq 1: U_n > U_{n-1}\},
$$

则$E(\gamma) = \mathrm e$。解答可见[【趣题分享】如何数学推导三国杀王荣吉占摸牌的期望值？（Web Premiere）_一只热爱奔跑的程序猿-CSDN博客](https://blog.csdn.net/CY19980216/article/details/121804278)，与本问题完全类似。

### 方法二：离散动态规划法

考虑这样一个问题：从$\{1,2,\dots,n-1\}$这$n-1$个数中等概率地抽取一个数若干次，直至抽取的这些数的和第一次大于$n$为止，抽取次数的数学期望。当$n \to \infty$时，就是我们想要的等价问题（两个问题的等价性显然，然而不会证明）。我们先讨论$n \neq \infty$的情形。

仍然考虑一般化的情形。从$\{1,2,\dots,n-1\}$这$n-1$个数中等概率地抽取一个数$X$次，直至抽取的这些数的和第一次大于$m$为止，记抽取次数的数学期望为

$$
EX(m).
$$

它是一个关于$m$的函数。初值条件为$EX(0)=1$。

对于任意一次抽取，要想使本次抽取结束后终于满足条件——这些数的和第一次大于$m$，则可由$n-1$条路径得到状态转移：

$$
\begin{aligned}
EX(m) &= \frac{1+EX(m-1)}{n-1} + \frac{1+EX(m-2)}{n-1} + \dots + \frac{1+EX(m-(n-1))}{n-1}.\\
&= 1 + \frac{1}{n-1}\sum_{i=1}^{n-1} EX(m-i) \\
&= 1 + \frac{1}{n-1}\sum_{i=m-n+1}^{m-1} EX(i).
\end{aligned}
$$

令上式$m = m-1$，两式做差得到

$$
EX(m) - EX(m-1) = \frac{1}{n-1}(EX(m-1) - EX(m-n)),
$$

若$m < n$，就有$EX(m-n)=0$，于是

$$
EX(m) = \frac{n}{n-1}EX(m-1).
$$

于是

$$
EX(m) = \left( \frac{n}{n-1} \right)^m EX(0) = \left( \frac{n}{n-1} \right)^m, \forall m < n.
$$

如果我们记$m = n - \varepsilon$，其中$\varepsilon > 0$，那么

$$
EX(n - \varepsilon) = \left( \frac{n}{n-1} \right)^{n - \varepsilon},
$$

当$n \to \infty$时，上式$\to \mathrm e$。

### 方法三：计算首中时的分布

当然，也可以直接暴力计算$P(\xi = n)$的表达式，然后利用$E(\xi) = \sum_{n=1}^{\infty} n P(\xi = n)$求解期望。

记$Y_n = \sum_{i=1}^n U_i$，则

$$
\begin{aligned}
P(\xi = n) &= P(Y_{n-1} \leq x, Y_n > x)\\
&= P(Y_{n-1} \leq x, Y_{n-1} + U_n > x) \\
&= P(Y_{n-1} \leq x, U_n > x - Y_{n-1}) \\
&= \int_{0}^x P(t \leq Y_{n-1} \leq t + \mathrm dt, U_n > x - t), \\
&= \int_{0}^x P(t \leq Y_{n-1} \leq t + \mathrm dt)P(U_n > x - t), \\
&= \int_0^x f_{Y_{n-1}}(t) \, \mathrm dt \cdot \left(1 - \int_{0}^{x-t} f_U(t) \, \mathrm dt \right) \\
&= \int_0^x f_{Y_{n-1}}(t)(1-x+t)\, \mathrm dt \\
&= \int_0^x \frac{t^{n-2}}{(n-2)!} (1-x+t) \, \mathrm dt \\
&= \frac{x^{n-1}(n-x)}{n!}.
\end{aligned}
$$

其中$f_{Y_{n-1}}$为$n-1$阶[Irwin-Hall分布](https://en.wikipedia.org/wiki/Irwin%E2%80%93Hall_distribution)的概率密度函数（$x \in [0, 1]$），$f_U$为$U(0,1)$的概率密度函数。

之后容易验证$E(\xi) = \mathrm e^x$。
