import params_function as pf

if __name__ == "__main__":
    # 获取初始参数
    params = pf.init_params
    # 分析
    result1 = pf.core_thermal_analysis(params)
    result2 = pf.steam_generator_analysis(params)
    result3 = pf.primary_loop_analysis(params)
    # 输出结果
    pf.output(result1, result2, result3)
    # 绘图
    pf.plot_results(result1, result2, result3)
