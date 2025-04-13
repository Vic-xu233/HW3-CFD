import numpy as np
import matplotlib.pyplot as plt

def compute_lax_error(Nt,u,u_all,C):
    for n in range(Nt):
      u_next = np.zeros_like(u)
      u_all[n, :] = u.copy()
      u_next = 0.5 * (np.roll(u, -1) + np.roll(u, 1)) - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1))#迭代
      u = u_next.copy()
    
    return u,u_all

def showplt(x,u0,u_exact,u,u_all,T,Nt):
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

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(X, T_mesh, u_all, cmap='viridis', shading='auto')
    plt.colorbar(label='u(x,t)')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.title('Lax格式下 u(x,t) 的二维伪彩色图')
    plt.tight_layout()
    plt.show()

# 空间
a = 1.0                     # 波速（常数）
L = 3.0                     # 空间总长
# 网格数量
N_values = [50, 100,150, 200, 400,600,800,1000]
dx_list = []
error_list = []

# 时间
C = 0.8                    # CFL = a*dt/dx
T = 3.0                     # 总模拟时间

for Nx in N_values:
    dx = L / Nx                 # 步长
    
    dt = C * dx / a
    Nt = int(T / dt)            # 时间网格数量
    x = np.linspace(0, L, Nx, endpoint=False)
    # 初始条件：u(x,0) = sin(2πx)
    u = np.sin(2 * np.pi * x/L)
    u0 = u.copy()  # 保存初始解
    u_all = np.zeros((Nt, Nx))  # 储存每一时刻的 u

     #Lax格式
    u,u_all=compute_lax_error(Nt,u,u_all,C)
    
    # 精确解
    u_exact = np.sin(2 * np.pi * (x - a * T)/L)
     
    # 误差计算（L2范数）
    err = np.sqrt(np.sum((u - u_exact)**2)*dx )

    #showplt(x,u0,u_exact,u,u_all,T,Nt)

    dx_list.append(dx)
    error_list.append(err)
    
    print(f"Nx = {Nx}, dx = {dx:.5f}, L2误差 = {err:.5e}")




# log-log 拟合
log_dx = np.log(dx_list)
log_err = np.log(error_list)
p = np.polyfit(log_dx, log_err, 1)[0]
print('拟合斜率 =',p)
# 可视化
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(6, 4))
plt.plot(log_dx, log_err, 'o-', label=f'拟合斜率 ≈ {p:.2f}')
plt.xlabel('log(Δx)')
plt.ylabel('log(L2误差)')
plt.title('Lax格式空间精度阶验证')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()