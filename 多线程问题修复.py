# 多线程问题修复——race condition
import time
import threading
count = 0
lock = threading.Lock()  # 锁
def add():
    global count
    for _ in range(100):
        with lock:  # 加锁
            tmp = count + 1
            time.sleep(0.000001)
            count = tmp + 1

threads = []

for _ in range(5):
    t = threading.Thread(target=add)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("最终 count =", count)

"""
① 多线程在 Python 中不能提升 CPU 性能（GIL 限制）
② 但会提升 IO 性能（非阻塞，切换更快）
③ 共享变量竞争会导致数值丢失 → race condition
④ 用 Lock / RLock 就能解决共享数据写冲突
"""