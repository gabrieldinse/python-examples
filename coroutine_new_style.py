# Author: gabri
# File: coroutine_new_style
# Date: 03/09/2019
# Made with PyCharm

# Standard Library
import asyncio

# Third party modules

# Local application imports


async def coroutine(delay):
    await asyncio.sleep(delay)
    print('done')


async def main():
    task1 = asyncio.create_task(coroutine(1))
    task2 = asyncio.create_task(coroutine(2))
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
