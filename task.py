import random
import subprocess
import time
import psutil
import numpy as np
import matplotlib.pyplot as plt

# 生成随机测试数据
def generate_test_data(size, data_type='float'):
    if data_type == 'float':
        return [random.uniform(0, 100000) for _ in range(size)]
    elif data_type == 'int':
        return [random.randint(0, 100000) for _ in range(size)]
    else:
        raise ValueError("data_type 必须是 'float' 或 'int'")

# 调用外部程序进行排序
def sort_data_external(data):
    input_data = "\n".join(map(str, data))
    start_time = time.time()
    
    mem_usage_before = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
    
    # 记录初始 CPU 使用率
    psutil.cpu_percent(interval=0)  # 先调用一次以重置计时器
    time.sleep(0.1)  # 等待短暂时间以确保读取准确
    cpu_before = psutil.cpu_percent(interval=None)

    try:
        result = subprocess.run(
            ["./sort_program"],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"排序程序执行失败，错误信息：{e}")
        return [], 0, 0
    except Exception as e:
        print(f"发生意外错误：{e}")
        return [], 0, 0

    mem_usage_after = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
    cpu_after = psutil.cpu_percent(interval=None)
    end_time = time.time()
    
    sorted_data = list(map(float, result.stdout.split()))
    sort_time = end_time - start_time
    mem_change = mem_usage_after - mem_usage_before
    cpu_usage = cpu_after - cpu_before
    
    return sort_time, mem_change, cpu_usage

# 可视化性能数据
def plot_performance(sizes, times, mem_changes, cpu_usages):
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    
    ax1.spines['right'].set_position(('outward', 60))  # 调整右侧坐标轴位置
    ax2.spines['right'].set_position(('outward', 120))  # 调整第二个右侧坐标轴位置

    ax1.plot(sizes, times, 'g-', label='排序时间 (秒)')
    ax2.plot(sizes, mem_changes, 'b-', label='内存变化 (MB)')
    ax3.plot(sizes, cpu_usages, 'r-', label='CPU 使用率 (%)')

    ax1.set_xlabel('数据集大小')
    ax1.set_ylabel('排序时间 (秒)', color='g')
    ax2.set_ylabel('内存变化 (MB)', color='b')
    ax3.set_ylabel('CPU 使用率 (%)', color='r')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax3.legend(loc='lower right')

    plt.title('排序性能表现')
    plt.show()

# 输出统计数据到文件
def write_statistics_to_file(sizes, times, mem_changes, cpu_usages):
    with open('performance_statistics.txt', 'w') as f:
        f.write("数据集大小\t排序时间 (秒)\t内存变化 (MB)\tCPU 使用率 (%)\n")
        for size, time, mem_change, cpu_usage in zip(sizes, times, mem_changes, cpu_usages):
            f.write(f"{size}\t{time:.4f}\t{mem_change:.2f}\t{cpu_usage:.2f}\n")

# 生成不同规模的数据集并排序
def main():
    dataset_sizes = [10000, 100000, 1000000,5000000,10000000,50000000]  # 数据集规模
    num_runs = 10  # 设置运行次数
    times = []
    mem_changes = []
    cpu_usages = []

    for size in dataset_sizes:
        print(f"\n生成 {size} 条数据...")
        total_time = 0
        total_mem_change = 0
        total_cpu_usage = 0
        
        for run in range(num_runs):
            print(f"运行 {run + 1}/{num_runs}...")
            data = generate_test_data(size)
            sort_time, mem_change, cpu_usage = sort_data_external(data)
            total_time += sort_time
            total_mem_change += mem_change
            total_cpu_usage += cpu_usage

        # 计算平均值
        avg_time = total_time / num_runs
        avg_mem_change = total_mem_change / num_runs
        avg_cpu_usage = total_cpu_usage / num_runs

        print(f"平均排序时间：{avg_time:.4f} 秒，平均内存变化：{avg_mem_change:.2f} MB，平均 CPU 使用率：{avg_cpu_usage:.2f}%")
        times.append(avg_time)
        mem_changes.append(avg_mem_change)
        cpu_usages.append(avg_cpu_usage)

    plot_performance(dataset_sizes, times, mem_changes, cpu_usages)
    write_statistics_to_file(dataset_sizes, times, mem_changes, cpu_usages)

if __name__ == "__main__":
    main()
