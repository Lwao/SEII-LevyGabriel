import asyncio

async def main():
    print('Started')
    task = asyncio.create_task(foo('Executing'))
    print('Finished')

async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(main())