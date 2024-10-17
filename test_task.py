import random
import subprocess
import time

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
    """
    调用已编译好的外部排序程序，并将数据传递给它进行排序。
    
    参数：
    data: 待排序的数据列表
    
    返回：
    排序后的数据列表，排序所用时间（秒）
    """
    # 将数据转换为字符串，并通过空格或换行符分隔
    input_data = "\n".join(map(str, data))
    
    # 使用 subprocess 调用外部排序程序
    start_time = time.time()
    
    # 调用可执行文件，并通过 stdin 传递数据，捕获 stdout 结果
    result = subprocess.run(
        ["./sort_program"],  # 可执行文件路径
        input=input_data,    # 传递给可执行程序的输入数据
        text=True,           # 输入和输出均为文本
        capture_output=True, # 捕获输出
        check=True           # 如果执行失败，则抛出异常
    )
    
    end_time = time.time()
    
    # 将结果拆分为列表
    sorted_data = list(map(float, result.stdout.split()))
    
    sort_time = end_time - start_time
    return sorted_data, sort_time

# 生成不同规模的数据集并排序
def main():
    dataset_sizes = [1000, 10000, 100000]  # 数据集规模：从 1 千到 100 千
    data_type = 'float'  # 生成浮点数数据
    for size in dataset_sizes:
        print(f"\n生成 {size} 条 {data_type} 数据...")
        data = generate_test_data(size, data_type)
        
        print(f"开始对 {size} 条数据进行排序（使用外部程序）...")
        sorted_data, sort_time = sort_data_external(data)
        
        print(f"完成排序，耗时：{sort_time:.4f} 秒")
        
if __name__ == "__main__":
    main()
