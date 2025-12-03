'''
并发（Concurrency）和并行（Parallelism）是两个概念.
并发是指任务交替执行，并行则是真的同时执行多个任务。
Python中常见的多线程是threading，但Python是解释型语言+全局解释器锁（GIL），
即便多线程也不能并行跑多个CPU密集任务，只能处理I/O密集型任务，比如文件读写、网络请求等等。
因此有了multiprocessing模块，此外我们会介绍下asyncio，这也是一个处理并发任务的工具。
'''

import asyncio
import multiprocessing
import threading
import time

num = 0
lock = threading.Lock()  # 锁


# 我们用task1来模拟一个需要等待的任务
def task1(name):
    global num
    print(f"{name}启动！")
    for _ in range(100):
        tmp = num + 1  # 模拟参数传递
        time.sleep(0.000001)  # 模拟等待
        num = tmp
    time.sleep(1)
    print(f"{name}终止！")


# 我们用task2来模拟一个需要等待的加锁的任务
def task2(name):
    global num
    print(f"{name}启动！")
    for _ in range(100):
        with lock:
            tmp = num + 1  # 模拟参数传递
            time.sleep(0.000001)  # 模拟等待
            num = tmp
    time.sleep(1)
    print(f"{name}终止！")


if __name__ == "__main__":

    print("##############测试1：threading测试。##############")
    # #################################未启用threading###########################################
    start_time = time.time()
    for i in range(5):
        task1(f"任务1_{i}")
    end_time = time.time()
    print(f"不启用threading，耗时为{end_time - start_time},num为{num}。")
    # 输出：不启用threading，耗时为12.737160921096802,num为500。
    # 总结：结果正确，但是耗时太久。

    # #################################启用threading-1###########################################
    num = 0
    start_time = time.time()
    threads = []
    for i in range(5):
        t = threading.Thread(target=task1, args=(f"任务1_{i}",))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"启用threading，共享变量导致race condition，耗时为{end_time - start_time},num为{num}。")
    # 输出：启用threading，共享变量导致race condition，耗时为2.552227258682251,num为100。
    # 结果错误，理想状态是500，但是耗时确实变短，说明在并发执行。

    # #################################启用threading-2###########################################
    num = 0
    start_time = time.time()
    threads = []
    for i in range(5):
        t = threading.Thread(target=task2, args=(f"任务1_{i}",))  # 我们这儿使用加锁的任务
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"启用threading，共享变量导致race condition，耗时为{end_time - start_time},num为{num}。")
    # 输出：启用threading，共享变量导致race condition，耗时为8.729201078414917,num为500。
    # 结果正确，理想状态是1000，但是锁导致共享数据计算时无法并发。

    # ① 多线程在 Python 中不能提升 CPU 性能（GIL 限制）
    # ② 但会提升 IO 性能（非阻塞，切换更快）
    # ③ 共享变量竞争会导致数值丢失 → race condition
    # ④ 用 Lock / RLock 就能解决共享数据写冲突

    print("##############测试2：threading测试。##############")
    num = 0
    start_time = time.time()
    threads = []
    for i in range(5):
        t = threading.Thread(target=task2, args=(f"任务1_{i}",))  # 我们这儿使用加锁的任务
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"启用threading，共享变量导致race condition，耗时为{end_time - start_time},num为{num}。")
    # 输出：启用threading，共享变量导致race condition，耗时为8.729201078414917,num为500。
    # 结果正确，理想状态是1000，但是锁导致共享数据计算时无法并发。
