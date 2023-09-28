import platform

import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://wttr.in') as response:
            html = await response.text()
            print(html)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())