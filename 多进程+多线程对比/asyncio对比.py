import asyncio
import multiprocessing
import threading
import time

num = 0

# 我们用task1来模拟一个需要等待的io
def task1(name):
    global num
    print(f"{name}启动！")
    for _ in range(100):
        tmp = num + 1  # 模拟参数传递
        time.sleep(0.000001)  # 模拟等待
        num = tmp
    time.sleep(1)
    print(f"{name}终止！")


# 我们用task2来模拟一个async任务
async def task2(name):
    global num
    print(f"{name}启动！")
    for _ in range(100):
        tmp = num + 1  # 模拟参数传递
        time.sleep(0.000001)  # 模拟等待
        num = tmp
    await asyncio.sleep(1)
    print(f"{name}终止！")


if __name__ == "__main__":

    print("##############测试1：asyncio测试。##############")
    # #################################未启用threading###########################################
    start_time = time.time()
    for i in range(5):
        task1(f"任务1_{i}")
    end_time = time.time()
    print(f"不启用asyncio，耗时为{end_time - start_time}。{num}")
    # 输出：不启用asyncio，耗时为12.794413805007935。500

    # #################################启用asyncio###########################################
    num = 0
    async def main():
        start_time = time.time()
        tasks = [
            asyncio.create_task(task2("任务1_1")),
            asyncio.create_task(task2("任务1_2")),
            asyncio.create_task(task2("任务1_3")),
            asyncio.create_task(task2("任务1_4")),
            asyncio.create_task(task2("任务1_5")),
        ]
        await asyncio.gather(*tasks)
        end_time = time.time()
        # gather表示多任务并发执行+收集结果
        print(f"启用asyncio，耗时为{end_time - start_time}。{num}")
    asyncio.run(main())  # 创建并运行
    # 输出：启用asyncio，耗时为8.754891157150269。500
