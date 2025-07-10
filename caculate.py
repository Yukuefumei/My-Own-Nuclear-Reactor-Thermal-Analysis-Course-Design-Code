import matplotlib.pyplot as plt
import numpy as np
from math import pi

#首先把plt的字体设置为黑体，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

# 示例数据：6组体积流量（m^3/h）、温度（℃）、压降（kPa）
data = np.array([
    [2.49,  34.4,  4.04],   # [体积流量, 温度, 压降]
    [2.17,  34.8,  3.37],
    [1.24,  34.9,  1.82],
    [0.84,  35.1,  1.37],
    [0.53,  35.1,  1.34],
    [2.89,  35.5,  5.03]
])

# data的每一行分别为：[体积流量(m^3/h), 温度(℃), 压降(kPa)]

def calculate(data):
    d = 0.02 # 管道直径（m）
    rho = 994 # 水的密度
    mu1 = 0.7411e-3 # 水在34℃的动力粘度（Pa.s）
    mu2 = 0.7263e-3 # 水在35℃的动力粘度（Pa.s）
    L = 1.3 # 管道长度（m），假设为1.3m
    result = np.zeros((data.shape[0], 3)) # 初始化结果数组
    for i in range(data.shape[0]):
        Q = data[i, 0] / 3600  # 体积流量 m^3/h 转 m^3/s
        v = Q / (pi * (d/2)**2)  # 流速 m/s
        mu = mu1 if i == 0 else mu2  # 只有第一行用mu1，其余用mu2
        Re = rho * v * d / mu  # 雷诺数
        p = data[i, 2] * 1000 # 压降转换为Pa
        # 采用达西-韦斯巴赫公式计算摩擦系数
        f =2* p * d / (L * rho * v**2)
        result[i, 0] = v
        result[i, 1] = Re
        result[i, 2] = f
    return result

def plot_moody(result):
    """
    绘制摩迪图，并在图上标注实验数据点
    参数：result - 包含流速、雷诺数、摩擦系数的数组
    """
    Re = np.logspace(3, 6, 500)
    # Blasius公式（光滑管，湍流区）
    f_blasius = 0.3164 / (Re ** 0.25)
    # 层流区理论解
    f_laminar = 64 / Re
    
    plt.figure(figsize=(8,6))
    plt.loglog(Re, f_laminar, 'b--', label='层流区 64/Re')
    plt.loglog(Re, f_blasius, 'r-', label='Blasius公式')
    # 绘制实验点
    plt.scatter(result[:,1], result[:,2], c='g', marker='o', label='实验数据')
    for i in range(result.shape[0]):
        plt.text(result[i,1], result[i,2], f'{i+1}', fontsize=9, ha='right')
    plt.xlabel('雷诺数 Re')
    plt.ylabel('摩擦系数 f')
    plt.title('穆迪图（Moody Diagram）')
    plt.legend()
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    res = calculate(data)
    print("流速(m/s)、雷诺数、摩擦系数：")
    print(res)
    plot_moody(res)
