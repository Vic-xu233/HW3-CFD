import numpy as np
import matplotlib.pyplot as plt

def compute_lax_error(Nt,u,u_all):
    for n in range(Nt):
      u_next = np.zeros_like(u)
      u_all[n, :] = u.copy()
      u_next = 0.5 * (np.roll(u, -1) + np.roll(u, 1)) - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1))#迭代
      u = u_next.copy()
    
    return u,u_all


# 空间
a = 1.0                     # 波速（常数）
L = 3.0                     # 空间总长
Nx = 100                    # 网格数量
dx = L / Nx                 # 步长
x = np.linspace(0, L, Nx, endpoint=False)

N_values = [50, 100, 200, 400, 800]
dx_list = []
error_list = []

# 时间
C = 1.5                     # CFL = a*dt/dx
dt = C * dx / a
T = 3.0                     # 总模拟时间
Nt = int(T / dt)            # 时间网格数量
for Nx in N_values:
    dx, err = compute_lax_error(Nx, C=0.5)  # 固定 CFL 为稳定值
    dx_list.append(dx)
    error_list.append(err)
    print(f"Nx = {Nx}, dx = {dx:.5f}, L2误差 = {err:.5e}")
# 初始条件：u(x,0) = sin(2πx)
u = np.sin(2 * np.pi * x)
u0 = u.copy()  # 保存初始解
u_all = np.zeros((Nt, Nx))  # 储存每一时刻的 u
# Lax格式
u,u_all=compute_lax_error(Nt,u,u_all)

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
# 构建网格用于3D绘图
t = np.linspace(0, T, Nt)
X, T_mesh = np.meshgrid(x, t)
'''
# 画3D图
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, T_mesh, u_all, cmap='viridis')

ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u(x,t)')
ax.set_title('Lax格式下 u(x,t) 的演化曲面图')
plt.tight_layout()
plt.show()
'''
plt.figure(figsize=(10, 6))
plt.pcolormesh(X, T_mesh, u_all, cmap='viridis', shading='auto')
plt.colorbar(label='u(x,t)')
plt.xlabel('x')
plt.ylabel('t')
plt.title('Lax格式下 u(x,t) 的二维伪彩色图')
plt.tight_layout()
plt.show()