package main

import (
	"log"
	"os"
)

// Fallback
const defaultAPIURL = "http://0.0.0.0:8000/predict"

// Config holds application configuration
type Config struct {
	APIURL string
}

// LoadConfig initializes configuration from environment variables
func LoadConfig() *Config {
	apiURL, exists := os.LookupEnv("API_URL")
	if !exists || apiURL == "" {
		log.Println("API_URL not found in environment, using default:")
		apiURL = defaultAPIURL
	}
	return &Config{APIURL: apiURL}
}
