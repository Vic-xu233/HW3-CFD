import numpy as np
import matplotlib.pyplot as plt

# 空间
a = 1.0                     # 波速（常数）
L = 3.0                     # 空间总长
Nx = 100                    # 网格数量
dx = L / Nx                 # 步长
x = np.linspace(0, L, Nx, endpoint=False)

# 时间
C = 0.5                     # CFL = a*dt/dx
dt = C * dx / a
T = 3.0                     # 总模拟时间
Nt = int(T / dt)            # 时间网格数量

# 初始条件：u(x,0) = sin(2πx)
u = np.sin(2 * np.pi * x)
u0 = u.copy()  # 保存初始解

# Lax格式
for n in range(Nt):
    u_next = np.zeros_like(u)
    u_next = 0.5 * (np.roll(u, -1) + np.roll(u, 1)) - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1))#迭代
    u = u_next.copy()

# 精确解
u_exact = np.sin(2 * np.pi * (x - a * T))

# 误差计算（L2范数）
error = np.sqrt(np.sum((u - u_exact)**2) * dx)
print(f"L2误差 = {error:.5e}")

# 可视化
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(8,4))
plt.plot(x, u0, '--', label='初始条件', linewidth=1)
plt.plot(x, u_exact, label='解析解')
plt.plot(x, u, 'o-', label='Lax格式数值解', markersize=3)
plt.xlabel('x')
plt.ylabel('u')
plt.title(f'Lax格式 t = {T}, C = {C}')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
