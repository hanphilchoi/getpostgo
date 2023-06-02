package main

import (
    "bufio"
    "fmt"
    "math/rand"
    "net/http"
    "os"
    "strings"
    "sync"
    "time"
)

func main() {
    var wg sync.WaitGroup
    var urls []string

    // Prompt for URLs
    fmt.Print("Enter URLs (separated by comma): ")
    reader := bufio.NewReader(os.Stdin)
    input, _ := reader.ReadString('\n')
    urls = strings.Split(strings.TrimSpace(input), ",")

    // Create a channel to receive responses
    responses := make(chan *http.Response)

    // Create a wait group for Go routines
    wg.Add(len(urls))

    // Create a client with random user agents and headers
    client := &http.Client{
        Timeout: time.Second * 10,
        Transport: &http.Transport{
            MaxIdleConnsPerHost: 100,
        },
    }

    // Start Go routines for each URL
    for _, url := range urls {
        go func(url string) {
            defer wg.Done()

            for i := 0; i < 5000; i++ {
                // Create a request with random user agents and headers
                req, err := http.NewRequest("GET", url, nil)
                if err != nil {
                    fmt.Println(err)
                    return
                }
                req.Header.Set("User-Agent", getRandomUserAgent())
                req.Header.Set("Accept-Language", "en-US,en;q=0.8")
                req.Header.Set("Connection", "keep-alive")

                // Send the request
                resp, err := client.Do(req)
                if err != nil {
                    fmt.Println(err)
                    return
                }

                // Send the response to the channel
                responses <- resp
            }
        }(url)
    }

    // Start a Go routine to print the status codes of responses
    go func() {
        for resp := range responses {
            fmt.Println(resp.StatusCode)
        }
    }()

    // Wait for all Go routines to finish
    wg.Wait()
    close(responses)
}

// getRandomUserAgent returns a random user agent string
func getRandomUserAgent() string {
    userAgents := []string{
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
    }
    return userAgents[rand.Intn(len(userAgents))]
}
