import numpy as np

# 原始数据
dx = np.array([0.06000, 0.03000, 0.02000, 0.00750, 0.00500, 0.00375, 0.00300])
L2_error = np.array([1.22032e+00, 1.14111e+00, 1.01842e+00, 5.95755e-01,
                     4.39255e-01, 3.46989e-01, 2.86512e-01])

# 取对数
log_dx = np.log(dx)
log_error = np.log(L2_error)

# 每两个点之间的斜率（局部误差阶）
slopes = np.diff(log_error) / np.diff(log_dx)

# 拟合整个斜率
fit_coef = np.polyfit(log_dx, log_error, 1)  # 返回 [k, b]
global_slope = fit_coef[0]

# 输出结果
print("对数 dx:", log_dx)
print("对数 L2 误差:", log_error)
print("每两个点之间的局部斜率:")
for i, s in enumerate(slopes):
    print(f"slope[{i}-{i+1}] = {s:.4f}")
print(f"\n拟合得到的整体斜率（误差阶估计）: {global_slope:.4f}")
