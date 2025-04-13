import numpy as np

# 错误参数设置（内存爆炸）
Nx = 10001
Nt = 53333
x = np.linspace(0, 1, Nx)
t = np.linspace(0, 1, Nt)

# 生成网格（立即触发内存错误）
X, T_mesh = np.meshgrid(x, t)  # 需要 3.97 GiB 内存
