import time

def task():
    total = 0
    for i in range(10000000):
        total += i * i
    return total

start = time.time()
task()
end = time.time()

print("单进程耗时：", end - start, "秒")
# 耗时0.4659s