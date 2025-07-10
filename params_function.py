import matplotlib.pyplot as plt
import numpy as np
import math

# 首先把plt的字体设置为黑体，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

init_params = [
    # [参数名称,         数值,    单位]
    ["反应堆热功率", 3e6, "W"],
    ["反应堆冷却剂入口温度", 250, "℃"],
    ["反应堆冷却剂出口温度", 750, "℃"],
    ["系统压力", 7e6, "Pa"],
    ["堆芯直径", 2.4, "m"],
    ["堆芯高度", 4.0, "m"],
    # 氦气物性，平均温度500℃
    ["密度", 0.48, "kg/m^3"],
    ["比热容", 5193, "J/(kg·K)"],
    ["动力粘度", 3.95e-5, "Pa·s"],
    ["导热系数", 0.304, "W/(m·K)"],
]

def core_thermal_analysis(params):
    """
    核心热工分析函数
    参数:
        params: 包含反应堆参数的数组
    返回:
        热工分析结果
    """
    # 提取参数
    power = float(params[0][1])  # 反应堆热功率 (W)
    T_in = float(params[1][1])   # 冷却剂入口温度 (℃)
    T_out = float(params[2][1])  # 冷却剂出口温度 (℃)
    H = float(params[5][1])  # 堆芯高度 (m)
    # 计算冷却剂质量流量
    density = float(params[6][1])  # 密度 (kg/m^3)
    cp = float(params[7][1])       # 比热容 (J/(kg·K))
    delta_T = T_out - T_in  # 温差 (K)
    k = float(params[9][1])  # 导热系数 (W/(m·K))
    mass_flow_rate = power / (cp * delta_T)  # 冷却剂质量流量 (kg/s)
    # 计算堆芯流通面积
    core_diameter = float(params[4][1])  # 堆芯直径 (m)
    core_area = math.pi * (core_diameter / 2) ** 2 * 0.4  # 堆芯流通面积 (m^2)，假设孔隙率为0.4
    # 计算堆芯流速
    flow_velocity = mass_flow_rate / (density * core_area)  # 堆芯流速 (m/s)
    # 计算雷诺数
    mu = float(params[8][1])  # 动力粘度 (Pa·s)
    D = 0.02 # 堆芯水力直径 (m)，假设为0.02m
    Re = (density * flow_velocity * D) / mu  # 雷诺数
    # 计算努塞尔数
    Pr = (cp * mu) / k  # 普朗特数
    Nu = 0.023 * Re**0.8 * Pr**0.3  # 努塞尔数
    # 计算传热系数
    h = Nu * k / D  # 传热系数 (W/(m^2·K))
    # 计算压降
    f = 0.02  # 假设摩擦因子为0.02
    delta_p = f * (H / D) * (density * flow_velocity**2 / 2)  # 压降 (Pa)
    # 汇总结果
    result = np.zeros(7)
    result[0] = mass_flow_rate      # 质量流量 (kg/s)
    result[1] = flow_velocity       # 堆芯流速 (m/s)
    result[2] = Re                  # 雷诺数
    result[3] = Pr                  # 普朗特数
    result[4] = Nu                  # 努塞尔数
    result[5] = h                   # 传热系数 (W/(m^2·K))
    result[6] = delta_p             # 压降 (Pa)
    return result

def steam_generator_analysis(params):
    """
    蒸汽发生器热工分析函数
    参数:
        params: 包含蒸汽发生器参数的数组
    返回:
        热工分析结果
    """
    # 提取参数
    power = float(params[0][1])  # 反应堆热功率 (W)
    T_in = float(params[1][1])   # 冷却剂入口温度 (℃)
    T_out = float(params[2][1])  # 冷却剂出口温度 (℃)
    U_SG = 800 # 蒸汽发生器传热系数 (W/(m^2·K))
    LMTD = (T_out - T_in) / math.log((T_out + 273.15) / (T_in + 273.15))  # 对数平均温差 (K)
    # 计算蒸汽发生器传热面积
    A_SG = power / (U_SG * LMTD)  # 蒸汽发生器传热面积 (m^2)
    # 管束参数
    D_tube_out = 0.019  # 管外径 (m)
    D_tube_in = 0.015  # 管内径 (m)
    L_tube = 4.0  # 管长 (m)
    # 计算管数
    A_tube = math.pi * D_tube_out * L_tube  # 单根管的外表面积 (m^2)
    n_tubes = A_SG / A_tube  # 管数
    # 计算管内流速
    density = float(params[6][1])  # 密度 (kg/m^3)
    cp = float(params[7][1])       # 比热容 (J/(kg·K))
    A_flow = math.pi * (D_tube_in / 2) ** 2  # 管内流通面积 (m^2)
    v_tube = (power / (cp * (T_out - T_in)))  # 管内流速 (m/s) 
    # 计算压降
    f = 0.02  # 假设摩擦因子为0.02
    delta_p_tube = f * (L_tube / (D_tube_in / 2)) * (density * v_tube**2 / 2)  # 管内压降 (Pa)
    result = np.zeros(5)
    result[0] = A_SG          # 蒸汽发生器传热面积
    result[1] = n_tubes       # 管数
    result[2] = v_tube        # 管内流速 (m/s)
    result[3] = delta_p_tube  # 管内压降 (Pa)
    result[4] = U_SG          # 蒸汽发生器传热系数 (W/(m^2·K))
    return result

def primary_loop_analysis(params):
    """
    主回路热工分析函数
    参数:
        params: 包含主回路参数的数组
    返回:
        热工分析结果
    """
    # 提取参数
    power = float(params[0][1])  # 反应堆热功率 (W)
    T_in = float(params[1][1])   # 冷却剂入口温度 (℃)
    T_out = float(params[2][1])  # 冷却剂出口温度 (℃)
    D_pipe_in = 0.4 # 主管道内径 (m)
    A_pipe = math.pi * (D_pipe_in / 2) ** 2
    # 计算流速
    density = float(params[6][1])  # 密度 (kg/m^3)
    cp = float(params[7][1])       # 比热容 (J/(kg·K))
    mass_flow_rate = power / (cp * (T_out - T_in))  # 冷却剂质量流量 (kg/s)
    flow_velocity = mass_flow_rate / (density * A_pipe)  # 主回路流速 (m/s)
    # 计算雷诺数
    mu = float(params[8][1])  # 动力粘度 (Pa·s)
    Re = (density * flow_velocity * D_pipe_in) / mu  # 雷诺数
    # 计算压降
    f = 0.02  # 假设摩擦因子为0.02
    L_pipe = 20 # 主管道长度 (m)
    dp = f * (L_pipe / D_pipe_in) * (density * flow_velocity**2 / 2)  # 压降 (Pa)
    dp_total = 50000 + 30000 + dp + 10000 # 已经假设提升压降、加速压降和局部压降
    result = np.zeros(4)
    result[0] = flow_velocity  # 主回路流速 (m/s)
    result[1] = Re            # 雷诺数
    result[2] = dp_total      # 总压降 (Pa)
    result[3] = dp            # 管道压降 (Pa)
    return result

def output(result1, result2, result3):
    """
    输出热工分析结果
    参数:
        result1: 核心热工分析结果
        result2: 蒸汽发生器热工分析结果
        result3: 主回路热工分析结果
    """
    print("核心热工分析结果:")
    print(f"质量流量: {result1[0]:.2f} kg/s")
    print(f"堆芯流速: {result1[1]:.2f} m/s")
    print(f"雷诺数: {result1[2]:.2f}")
    print(f"普朗特数: {result1[3]:.2f}")
    print(f"努塞尔数: {result1[4]:.2f}")
    print(f"传热系数: {result1[5]:.2f} W/(m^2·K)")
    print(f"压降: {result1[6]:.2f} Pa\n")

    print("蒸汽发生器热工分析结果:")
    print(f"传热面积: {result2[0]:.2f} m^2")
    print(f"管数: {result2[1]:.0f}")
    print(f"管内流速: {result2[2]:.2f} m/s")
    print(f"管内压降: {result2[3]:.2f} Pa")
    print(f"蒸汽发生器传热系数: {result2[4]:.2f} W/(m^2·K)\n")

    print("主回路热工分析结果:")
    print(f"主回路流速: {result3[0]:.2f} m/s")
    print(f"雷诺数: {result3[1]:.2f}")
    print(f"总压降: {result3[2]:.2f} Pa")
    print(f"管道压降: {result3[3]:.2f} Pa")

def plot_results(result1, result2, result3):
    """
    绘制热工分析结果图
    参数:
        result1: 核心热工分析结果
        result2: 蒸汽发生器热工分析结果
        result3: 主回路热工分析结果
    """
    plt.figure(1)
    plt.subplot(2, 2 ,1)
    labels = ['堆芯', '蒸汽发生器', '主回路']
    values = [result1[6], result2[3], result3[3]]
    plt.bar(labels, values)
    plt.title('压降分布')
    plt.xlabel('组件')
    plt.ylabel('压降 (Pa)')

    plt.subplot(2, 2, 2)
    temps = [250, 750, 750, 250] # 假设的温度分布
    plt.plot([0, 1, 2, 3], temps, '-o', linewidth=2)
    plt.title('一回路温度分布')
    plt.xlabel('位置')
    plt.ylabel('温度 (℃)')
    plt.xticks([0, 1, 2, 3], ['堆芯入口', '堆芯出口', '蒸汽发生器入口', '蒸汽发生器出口'])
    plt.grid(True)

    plt.subplot(2, 2, 3)
    velocities = [result1[1], result2[2], result3[0]]  # 流速对比
    plt.bar(labels, velocities)
    plt.title('流速分布')
    plt.xlabel('位置')
    plt.ylabel('流速 (m/s)')

    plt.subplot(2, 2, 4)
    plt.pie([result1[6], result2[3], result3[3]], labels=labels, autopct='%1.1f%%') # 压降占比
    plt.title('压降占比')
    plt.show()