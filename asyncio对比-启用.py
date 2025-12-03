import asyncio
import time

async def fetch(n):
    print(f"start {n}")
    await asyncio.sleep(1)
    # await表示这里要等一下，等待期间可以去执行别的事情。
    print(f"end {n}")
    return n

# async def定义了一个协程函数，调用这个函数不会直接执行代码，而是返回一个协程对象
#
async def main():
    start = time.time()

    tasks = [
        asyncio.create_task(fetch(1)),
        asyncio.create_task(fetch(2)),
        asyncio.create_task(fetch(3)),
    ]

    await asyncio.gather(*tasks)
    # gather表示多任务并发执行+收集结果

    print("总耗时:", time.time() - start)

asyncio.run(main())  # 创建并运行
