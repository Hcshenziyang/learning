# 多线程问题展示——race condition
import time
import threading
count = 0

def add():
    global count
    for _ in range(100):
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
理论上结果应该是1000，但是实际输出结果为202。
多个线程可能这样交错：
线程A: tmp = count + 1 → tmp=101
线程B: tmp = count + 1 → tmp=101
线程A: count = tmp + 1 → count=102
线程B: count = tmp + 1 → count=102   # 覆盖 A 的结果
"""