import asyncio
import threading
import time
from multiprocessing import Process, Queue


# 我们用task1来模拟一个需要复杂的计算任务
def task1():
    result = 0
    for i in range(100000000):
        result += i*i+i-(i+1)*(i-1)
    print(result)

def task2(start,end,q):
    result = 0
    for i in range(start,end):
        result += i*i+i-(i+1)*(i-1)
    print(result)
    q.put(result)  # 结果回传



if __name__ == "__main__":

    print("##############测试1：asyncio测试。##############")
    # #################################不启用mulyiprocessing###########################################
    start_time = time.time()
    task1()
    end_time = time.time()
    print(f"不启用mulyiprocessing，耗时为{end_time - start_time}。")
    # 输出：不启用mulyiprocessing，耗时为12.580572128295898。

    # #################################启用mulyiprocessing###########################################
    start_time = time.time()
    q = Queue()  # 通信通道
    processes = []
    nums = 100000000
    step = nums // 4  # 就是本来是100000000，现在拆分成四个任务，就是25000000每个

    for i in range(4):
        # 创建进程对象，任务，参数
        p = Process(target=task2, args=(i * step, (i + 1) * step, q))
        # 启动进程
        p.start()
        processes.append(p)

    for p in processes:
        # 等待进程结束
        p.join()

    result = sum(q.get() for _ in range(4))  # q.get收集结果

    print("结果:", result)
    end_time = time.time()
    print("多进程耗时：", end_time - start_time, "秒")
    # 输出：多进程耗时： 3.616527557373047 秒
