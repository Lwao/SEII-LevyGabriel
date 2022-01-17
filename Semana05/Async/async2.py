import asyncio

async def main():
    print('Started')
    await foo('Executing')
    print('Finished')

async def foo(text):
    print(text)
    await asyncio.sleep(1)

asyncio.run(main())