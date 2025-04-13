
# 📦 Lax格式求解线性对流方程并验证精度阶数

本项目基于 Python，使用有限差分方法中的 **Lax 格式** 求解一维线性对流方程，并验证其空间精度阶数，支持多分辨率误差分析和可视化输出。还可轻松切换为 Upwind 和 Lax-Wendroff 方法以对比不同格式的数值特性。

---

## 📐 模型简介

我们考虑的一维线性对流方程为：

\[
\frac{\partial u}{\partial t} + a \frac{\partial u}{\partial x} = 0, \quad x \in [0, L], \quad t > 0
\]

该方程描述随速度 \(a\) 向右传播的波。

---

## 🧠 数值格式

### ✅ Lax 格式

\[
u_j^{n+1} = \frac{1}{2}(u_{j+1}^n + u_{j-1}^n) - \frac{C}{2}(u_{j+1}^n - u_{j-1}^n)
\]

### ✅ Upwind 格式（a > 0）

\[
u_j^{n+1} = u_j^n - C (u_j^n - u_{j-1}^n)
\]

### ✅ Lax-Wendroff 格式

\[
u_j^{n+1} = u_j^n - \frac{C}{2}(u_{j+1}^n - u_{j-1}^n) + \frac{C^2}{2}(u_{j+1}^n - 2u_j^n + u_{j-1}^n)
\]

> 其中 Courant 数 \( C = \frac{a \Delta t}{\Delta x} \)，必须满足 \( C \leq 1 \) 保证显式格式稳定。

---

## 🧩 实现方式

在本代码中，核心的数值格式由一行代码控制。我们通过替换 `compute_*` 函数中的这句来实现不同格式：

### 🔁 Lax：
```python
u_next = 0.5 * (np.roll(u, -1) + np.roll(u, 1)) - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1))
```

### 🔁 Upwind：
```python
u_next = u - C * (u - np.roll(u, 1))
```

### 🔁 Lax-Wendroff：
```python
u_next = u - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1)) + 0.5 * C**2 * (np.roll(u, -1) - 2*u + np.roll(u, 1))
```

程序结构高度模块化，你只需替换 `compute_lax_error` 中的迭代语句或函数名即可切换格式。

---
## 📁 主要文件结构

- `compute_lax_error(Nt, u, u_all, C)`：Lax格式的数值迭代器，支持周期边界；
- `showplt(x, u0, u_exact, u, u_all, T, Nt, Nx)`：展示初始条件、数值解、解析解对比图 + u(x,t) 的伪彩色图；
- 主程序中：
  - 使用多组空间网格数量 `N_values`；
  - 自动计算每组对应的空间步长 `dx` 与 L2 误差；
  - 使用 `np.polyfit` 拟合 log-log 图，得到格式精度斜率。

---
## 📊 精度验证

程序自动使用多种空间分辨率 \( Nx \)，计算每次运行后的 L2 误差，并通过 log-log 拟合评估数值格式的空间精度阶数：

\[
\text{误差} \sim \mathcal{O}(\Delta x^p)
\]

输出如：

```
Nx = 100, dx = 0.03000, L2误差 = 2.13e-02
Nx = 200, dx = 0.01500, L2误差 = 1.07e-02
拟合斜率 ≈ 1.00 ✅
```

---

## 📈 可视化说明

| 图像 | 内容 |
|------|------|
| 曲线图 | 初始条件、解析解与数值解对比 |
| 伪彩色图 | 数值解 u(x,t) 随时间演化图 |
| log-log 图 | 拟合误差阶数（斜率） |

---

## ⚙️ 参数说明

| 参数 | 作用 | 建议设置 |
|------|------|----------|
| `a` | 波速 | 正数，如 `1.0` |
| `L` | 空间长度 | 如 `3.0` |
| `C` | Courant 数 | 0 < C ≤ 1 |
| `N_values` | 网格数量列表 | `[50, 100, 200, ..., 1000]` |
| `T` | 总模拟时间 | 一般为传播周期长度 |

---
## ⚠ 注意事项

- 若使用非常高分辨率（如 Nx=6000），由于 `u_all` 是三维数组，建议注释掉 `showplt()` 函数以避免内存溢出。
- 当前边界条件为**周期边界**，通过 `np.roll` 实现。
- 使用中文字体时确保系统已安装 SimHei 字体。

---

## ✅ 环境依赖

- Python 3.x
- numpy
- matplotlib

安装命令：
```bash
pip install numpy matplotlib
```

---

## 👨‍💻 作者

由用户撰写，ChatGPT 辅助生成注释与文档。
