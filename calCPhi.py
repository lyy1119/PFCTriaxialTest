import numpy as np
from scipy.optimize import minimize

def calculate_mohr_coulomb(data):
    """
    计算内摩擦角(phi)和内聚力(c)
    :param data: list of lists, [[sigma1_1, sigma3_1], [sigma1_2, sigma3_2], ...]
    :return: dict 包含 c (kPa/MPa), phi (degrees) 和拟合残差
    """
    # 1. 数据预处理，计算每个圆的圆心 (O) 和半径 (R)
    circles = []
    for s1, s3 in data:
        o = (s1 + s3) / 2.0
        r = (s1 - s3) / 2.0
        circles.append((o, r))

    # 2. 定义误差函数 (目标函数)
    # params[0] 是 c, params[1] 是 phi (弧度)
    def objective(params):
        c, phi_rad = params
        error = 0
        for o, r in circles:
            # 理论计算的半径应该接近圆心到直线的垂距
            # d = O*sin(phi) + c*cos(phi)
            d_calc = o * np.sin(phi_rad) + c * np.cos(phi_rad)
            error += (d_calc - r)**2
        return error

    # 3. 设置初始猜想值
    # 初始 phi 设为 30度, c 设为 10 (根据经验或简单线性回归预估)
    initial_guess = [10.0, np.radians(30)]

    # 4. 定义边界（c > 0, 0 < phi < pi/2）
    bounds = [(0, None), (0, np.pi/2)]

    # 5. 执行优化
    result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')

    if result.success:
        c_opt, phi_rad_opt = result.x
        return {
            "c": round(c_opt, 3),
            "phi_deg": round(np.degrees(phi_rad_opt), 3),
            "success": True,
            "residual": result.fun
        }
    else:
        return {"success": False, "message": "Optimization failed"}

# --- 测试代码 ---
# 示例数据：[[sigma1, sigma3], ...]
test_data = [
    [247, 100],
    [1260, 500],
    [1900, 800]
]

res = calculate_mohr_coulomb(test_data)
print(f"计算结果: 内聚力 c = {res['c']}, 内摩擦角 phi = {res['phi_deg']}°")