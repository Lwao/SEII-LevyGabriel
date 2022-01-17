import asyncio

async def main():
    print('Started')
    task = asyncio.create_task(foo('Executing'))
    await asyncio.sleep(0.5)
    print('Finished')

async def foo(text):
    print(text)
    await asyncio.sleep(10)

asyncio.run(main())