package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"strings"
	"time"
)

var publicProviders = map[string]bool{
	"gmail.com":      true,
	"yahoo.com":      true,
	"outlook.com":    true,
	"hotmail.com":    true,
	"icloud.com":     true,
	"aol.com":        true,
	"mail.com":       true,
	"protonmail.com": true,
}

const emailPattern = `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

func main() {
	emailRegex := regexp.MustCompile(emailPattern)
	client := &http.Client{Timeout: 10 * time.Second}

	var urls []string

	// Check if URLs were passed as system/command-line arguments
	if len(os.Args) > 1 {
		urls = os.Args[1:]
	} else {
		// Fallback to interactive prompt if no arguments are provided
		fmt.Print("Enter URLs separated by space: ")
		scanner := bufio.NewScanner(os.Stdin)
		if scanner.Scan() {
			urls = strings.Fields(scanner.Text())
		}
	}

	if len(urls) == 0 {
		fmt.Println("No URLs provided. Exiting.")
		return
	}

	for _, url := range urls {
		// Ensure valid URL scheme
		if !strings.HasPrefix(url, "http://") && !strings.HasPrefix(url, "https://") {
			url = "https://" + url
		}

		fmt.Printf("\n--- Scraping: %s ---\n", url)

		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			fmt.Printf("Error creating request: %v\n", err)
			continue
		}
		req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

		resp, err := client.Do(req)
		if err != nil {
			fmt.Printf("Error fetching URL: %v\n", err)
			continue
		}

		if resp.StatusCode != http.StatusOK {
			fmt.Printf("Error: server returned status %d\n", resp.StatusCode)
			resp.Body.Close()
			continue
		}

		bodyBytes, err := io.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			fmt.Printf("Error reading response: %v\n", err)
			continue
		}

		matches := emailRegex.FindAllString(string(bodyBytes), -1)

		if len(matches) == 0 {
			fmt.Println("No emails found.")
			continue
		}

		uniqueEmails := make(map[string]bool)
		for _, match := range matches {
			uniqueEmails[strings.ToLower(match)] = true
		}

		for email := range uniqueEmails {
			parts := strings.Split(email, "@")
			if len(parts) < 2 {
				continue
			}
			domain := parts[1]

			category := "Corporate/Custom"
			if publicProviders[domain] {
				category = "Public"
			}

			fmt.Printf("Email: %-30s | Type: %s\n", email, category)
		}
	}
}
