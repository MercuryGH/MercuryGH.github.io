---
title: 可微渲染实验：基于SDF的结果拟合
date: 2024-04-03 13:42:04
tags:
- 可微渲染
---

> Project: https://github.com/MercuryGH/diff-rendering-slang

在本次实验中，我们将调整一个圆（或其他图形）的半径、圆心和颜色，拟合一个给定的三角形，使得两个图形在像素覆盖性和颜色上的均方误差最小。

<!--more-->

## 预期结果

预期结果如下：

![result](./dr.gif)

可以看到圆不断靠近三角形的中心，并调整自身半径，以期自身与三角形的覆盖程度的一致性最高；圆的颜色同时也不断接近三角形的颜色。

## 实验平台

* [Slang-Python](https://github.com/shader-slang/slang-python/)，基于 soft-rasterizer-example

## 相关知识

### 可微的光栅化过程

为了让离散的光栅化过程连续化，从而方便自动微分，我们将判断一个像素是否在三角形内的逻辑修改为基于 SDF，并使用 sigmoid 函数

$$
\sigma(x) = \frac{1}{1 + \mathrm e^{-x/\sigma}} \in (0, 1)
$$

平滑计算出的有向距离，其中 $\sigma$ 是一个较固定的参数，控制 sigmoid 函数的“陡峭”程度。

具体而言，我们对每个像素计算其到当前圆的有向距离 $x$，其中 $x \in (-\infty, +\infty)$ ，若像素在圆内则取负值。随后，计算 $\sigma(-x)$ ，结果越大，则说明像素越接近圆心；反之像素越远离圆。对于 $x$ 在 $0$ 附近的边缘点，这一计算结果会给出接近 $\frac{1}{2}$ 的值。最后，我们用线性插值

$$
r = \text{lerp}(c_{\text{circle}}, c_{\text{bg}}, \sigma(-x))
$$

决定该点的颜色 $r$，其中 $c_{\text{circle}}, c_{\text{bg}}$ 分别为圆的颜色和背景色（白色）。由于 sigmoid 函数在 $x = 0$ 附近平滑且快速上升，因此光栅化结果会在边缘处存在明显的模糊现象。

可微光栅化的详尽实现还需要考虑多个三角形、深度剔除等，可参考[ SoftRas 的原始论文](https://arxiv.org/abs/1904.01786)。

### 学习过程

“学习”就是使用基于梯度的方法求解目标函数的局部最小值的过程。为了拟合给定的三角形，我们定义目标函数为

```
torch.mean((outputImage - targetImage) ** 2)
```

即圆图形与三角形图形之间的均方误差，这一误差是每像素累计计算的。

利用 slang 的自动微分，整个光栅化过程都是可微分的，因此梯度的后向传播成为可能。我们可以利用 torch 框架的 `torch.autograd.Function`，为学习循环（learning loop）的前向光栅化-后向梯度传播调用过程提供便利。详细可参考相关样例。


