---
title: 基于PD的弹性体仿真的并行算法
date: 2024-05-27 23:49:29
tags:
- 图形学
- 物理仿真
- GPU
---

> 本文是我的本科毕业设计（2023年提交）

由于包含大量排版格式，请直接查阅 PDF 格式的 [论文](ug_thesis.pdf) 阅读。

<!--more-->

## 开源代码与仿真结果

详见 [GitHub 页面](https://github.com/MercuryGH/pd-with-gpu)

---

本文章同时用于试验数学公式的排版，后续内容只是论文的其中一小节的节选，不需要阅读。

## 数学约定

给定一个顶点数为$n$的三维动力系统，记位置向量$\mathbf q \in\mathbb R^{3n}$，速度向量$\mathbf v \in\mathbb R^{3n}$，作用于各顶点的外力$\mathbf f_{ext} \in\mathbb R^{3n}$，内力$\mathbf f_{int}(\mathbf q) = -\sum_c \nabla_{\mathbf q} w_c(\mathbf q)$为一关于$\mathbf q$的函数，其中$w_c: \mathbb R^{3n} \to [0, +\infty)$为约束$c$的势能函数。运用牛顿第二定律，对时刻$t$到时刻$t+1$进行隐式积分得到

$$
\begin{aligned}
    \mathbf q_{t + 1} &= \mathbf q_t + h \mathbf v_{t + 1}, \\
    \mathbf v_{t + 1} &= \mathbf v_t + h \mathbf M^{-1}(\mathbf f_{int}(\mathbf q_{t+1}) + \mathbf f_{ext}),
    \end{aligned}
$$

其中$\mathbf M \in\mathbb R^{3n \times3n}$为质量矩阵，$h$为时间步长。将速度$\mathbf v_{t+1}$代回，得到

$$
\begin{aligned}
    & \mathbf M( \mathbf q_{t+1} - \mathbf q_t - h \mathbf v_t) = h^2( \mathbf f_{int}(\mathbf q_{t+1}) + \mathbf f_{ext}), \\
    \to & \mathbf M(\mathbf q_{t+1} - \mathbf q_t - h \mathbf v_t - h^2 \mathbf M^{-1} \mathbf f_{ext}) = h^2 \mathbf f_{int}( \mathbf q_{t+1}).
    \end{aligned}
$$

令

$$
\mathbf s_t = \mathbf q_t + h \mathbf v_t + h^2 \mathbf M^{-1} \mathbf f_{ext},
$$

它的物理意义为不考虑内力、碰撞等其他因素，顶点在当前状态下继续移动一时间步长后的位置。上式化为

$$
\mathbf M( \mathbf q_{t+1}- \mathbf s_t) = h^2 \mathbf f_{int}( \mathbf q_{t+1})
$$

该式传统上可使用牛顿迭代法求解

$$
\mathbf M( \mathbf q^{(k+1)}- \mathbf s_t) = h^2( \mathbf f_{int}( \mathbf q^{(k)} ) + \mathbf K( \mathbf q^{(k)})(\mathbf q^{(k+1)} - \mathbf q^{(k)}) )
$$

其中，迭代初值$\mathbf q^{(0)} = \mathbf q_{t+1}$，$\mathbf K(\mathbf q^{(k)}) = \frac{\partial\mathbf f_{int}}{\partial\mathbf q}$为在$\mathbf q^{(k)}$处的Hessian（物理上是刚性矩阵）。这一方法收敛较快，但计算Hessian的代价很大，现已不再通行。PD重新考虑了这一式子，将其看作一个优化问题：

$$
\arg \min_{\mathbf q_{t+1}} \frac{1}{2h^2}|| \mathbf M^{1/2} ( \mathbf q_{t+1}- \mathbf s_t)||^2 + \sum_c w_c( \mathbf q_{t+1})
$$

可见，$|| \mathbf M^{1/2} ( \mathbf q_{t+1}- \mathbf s_t)||^2$一项希望最小化$\mathbf q_{t+1}$与$\mathbf s_t$的“距离”，而$\sum_c w_c( \mathbf q_{t+1})$则希望最小化约束势能。PD进一步基于超弹性假设指出，势能项$w_c( \mathbf q_{t+1})$具有二次形式

$$
\sum_c w_c( \mathbf q_{t+1}) = \sum_c \frac{\omega_c}{2} || \mathbf A_c \mathbf q - \mathbf A_c' \mathbf p_c||^2,
$$

其中$\omega_c$是约束$c$的正权重，$\mathbf p_c$是$\mathbf q$在约束$c$上的使势能为零的投影，$\mathbf A_c$和$\mathbf A_c'$为两个与$c$的类型有关的常量矩阵，描述$\mathbf q$与$\mathbf p_c$的关系。例如，若$c$是一个弹簧，则$\mathbf A_c \mathbf q \in\mathbb R^3$表示模拟时，弹簧两端顶点之间的位移向量，而$\mathbf A_c' \mathbf p_c \in\mathbb R^3$则表示弹簧处于原长时，两端顶点之间的位移向量，如此，模拟时弹簧的弹性势能可由$w_c(\mathbf q_{t+1})$描述。基于该模型，PD将主要求解过程分成两步：

* **局部约束求解**（local solve, local step）。这一步将当前位置$\mathbf q$根据各约束$c$投影到$\mathbf p_c$，求解优化问题

  $$
  \min_{\mathbf p_c} \frac{\omega_c}{2} ||\mathbf A_c \mathbf q - \mathbf A_c' \mathbf p_c||^2.
  $$
* **全局线性系统求解**（global solve, global step）。这一步利用local step获取的各约束投影$\mathbf p_c$求解一个线性方程组。具体地，通过令最小化式子的梯度为零，可以得到如下的线性方程组

  $$
  \left(\frac{\mathbf M}{h^2} + \sum_c \omega_c \mathbf A_c^T \mathbf A_c \right) \mathbf x = \frac{\mathbf M}{h^2} \mathbf s_t + \sum_c \omega_c \mathbf A_c^T \mathbf A_c' \mathbf p_c.
  $$

  其中，系数矩阵$\mathbf A=\frac{\mathbf M}{h^2} + \sum_c \omega_c \mathbf A_c^T \mathbf A_c$是常量实对称矩阵，因此可预计算。原始的PD框架即使用基于Cholesky分解的直接法求解该线性方程组，而本仿真器则支持Cholesky分解直接法和Jacobi迭代法两种算法进行求解。

求解$\mathbf x$后，PD的一次迭代即完成，令$\mathbf q_{t+1} = \mathbf x$，即进入下一次迭代。迭代达到最大次数后即完成，更新各顶点的位置和速度。

PD算法框架中，需要仿真的弹性体均包含若干约束，因此需要在仿真之前对这些约束进行预计算，以高效地完成每次local-global迭代。因此，本仿真器的求解过程将主要包括如下两部分：

* **预计算**，包括局部约束的预计算以及全局线性方程组系数矩阵的预计算，这一步在工业软件中也常被称为“烘焙”。在预计算流程中，首先将根据模型的$\mathbf M$，不同约束的$\omega_c \mathbf A_c^T \mathbf A_c$预构建系数矩阵$\mathbf A$，并预计算global step中的线性求解器。同时，若用户要求使用GPU进行local step，则求解器还需要将所有约束拷贝至GPU内存。
* **PD仿真**。
