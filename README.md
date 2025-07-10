# 反应堆热工课程设计 Python 仿真程序

## 项目简介
本项目为核反应堆热工课程设计的仿真分析工具，基于 Python 实现，包含核心热工分析、蒸汽发生器分析、主回路分析及可视化功能。基于月背3MW的氦冷反应堆系统的热工参数计算与结果展示。

## 主要功能
- **核心热工分析**：计算堆芯质量流量、流速、雷诺数、普朗特数、努塞尔数、传热系数、压降等。
- **蒸汽发生器分析**：计算传热面积、管数、管内流速、管内压降、传热系数等。
- **主回路分析**：计算主回路流速、雷诺数、总压降、管道压降等。
- **结果输出与可视化**：终端输出主要热工参数，自动生成压降分布、温度分布、流速分布、压降占比等图表。

## 文件结构
- `params_function.py`：主要参数定义与各类热工分析函数、可视化函数。
- `main.py`：主程序入口，调用分析与输出、绘图函数。

## 依赖环境
- Python 3.7 及以上
- numpy
- matplotlib

安装依赖：
```powershell
pip install numpy matplotlib
```

## 使用方法
1. 确保 `params_function.py` 和 `main.py` 在同一目录下。
2. 运行主程序：
   ```powershell
   python main.py
   ```
3. 程序将输出各环节热工参数，并弹出可视化图表。

## 参数说明
初始参数在 `params_function.py` 的 `init_params` 中定义，包括：
- 反应堆热功率、冷却剂进出口温度、系统压力、堆芯尺寸、氦气物性参数等。
如需修改工况，可直接编辑 `init_params`。

## 主要函数说明
- `core_thermal_analysis(params)`：核心热工分析。
- `steam_generator_analysis(params)`：蒸汽发生器分析。
- `primary_loop_analysis(params)`：主回路分析。
- `output(result1, result2, result3)`：终端输出分析结果。
- `plot_results(result1, result2, result3)`：绘制结果图表。

## 结果示例
- 质量流量、流速、雷诺数、压降等数值输出
- 压降分布柱状图、温度分布折线图、流速分布柱状图、压降占比饼图

## 备注
- 支持中文显示，已设置 matplotlib 字体。
- 适合教学、课程设计、参数敏感性分析等用途。
