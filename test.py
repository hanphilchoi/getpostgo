import asyncio
import aiohttp
import random
from fake_useragent import UserAgent
from termcolor import colored

async def fetch(session, url):
    headers = {'User-Agent': UserAgent().random}
    async with session.get(url, headers=headers) as response:
        return response.status, await response.text()

async def bound_fetch(sem, session, url):
    async with sem:
        return await fetch(session, url)

async def run(url):
    tasks = []
    sem = asyncio.Semaphore(5000)
    async with aiohttp.ClientSession() as session:
        for i in range(5000):
            task = asyncio.ensure_future(bound_fetch(sem, session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

if __name__ == '__main__':
    url = input("Enter a URL: ")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(url))
    responses = loop.run_until_complete(future)
    for status, text in responses:
        if status == 200:
            print(colored(f"Request successful with status code {status}", "green"))
        else:
            print(f"Request failed with status code {status}")
