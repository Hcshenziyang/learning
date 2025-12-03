import time
from multiprocessing import Process, Queue

def task(start, end, q):
    total = 0
    for i in range(start, end):
        total += i * i
    q.put(total)  # 结果回传

if __name__ == "__main__":
    # windows必须写if __name__，否则会递归启动无限子进程。
    start_time = time.time()

    q = Queue()  # 通信通道
    processes = []
    nums = 10000000
    step = nums // 4     # 就是本来是10000000，现在拆分成四个任务，就是2500000每个

    for i in range(4):
        # 创建进程对象，任务，参数
        p = Process(target=task, args=(i*step, (i+1)*step, q))
        # 启动进程
        p.start()
        processes.append(p)

    for p in processes:
        # 等待进程结束
        p.join()

    result = sum(q.get() for _ in range(4))  # q.get收集结果

    print("结果:", result)
    print("多进程耗时：", time.time() - start_time, "秒")
    # 耗时0.2333s