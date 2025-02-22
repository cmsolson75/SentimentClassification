package main

import (
	"log"
	"os"
)

// defaultAPIURL is the fallback API endpoint if API_URL is not set.
const defaultAPIURL = "http://0.0.0.0:8000/predict"

// Config holds application configuration settings
type Config struct {
	APIURL string
}

// LoadConfig initializes configuration from environment variables
//
// If API_URL is not set, it falls back to defaultAPIURL.
// Logs a warning if the environment variable is missing.
//
// Returns:
//   - A pointer to a Config struct containing the API URL.
func LoadConfig() *Config {
	apiURL, exists := os.LookupEnv("API_URL")
	if !exists || apiURL == "" {
		log.Println("API_URL not found in environment, using default:")
		apiURL = defaultAPIURL
	}
	return &Config{APIURL: apiURL}
}
