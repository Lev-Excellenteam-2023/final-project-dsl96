import asyncio


async def get_presentation(path):
    print('')
    print(f'{path} start')
    await asyncio.sleep(20)
    print(path)
    print('')
    print(f'{path} end')


async def async_input(text_to_user):
    loop = asyncio.get_running_loop()
    print('')
    user_input = await loop.run_in_executor(None, input, text_to_user)
    return user_input


async def main():
    while True:
        path = await async_input("enter path to pttx")

        if path == 'E':
            return
        asyncio.create_task( getPresentation(path) )

if __name__ == '__main__':
    asyncio.run(main())



