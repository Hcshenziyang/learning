import time

def fetch(n):
    print(f"start {n}")
    time.sleep(1)
    print(f"end {n}")
    return n

start = time.time()

fetch(1)
fetch(2)
fetch(3)

print("总耗时:", time.time() - start)
