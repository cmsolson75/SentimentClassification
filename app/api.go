package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// SentimentResponse represents the sentiment classification result returned by the API.
type SentimentResponse struct {
	Label      string  `json:"label"`
	Confidence float64 `json:"confidence"`
}

// APIError is a custom error type for handing API request errors.
type APIError struct {
	Message string
	Err     error
}

// Error implements the error interface for APIError.
func (e *APIError) Error() string {
	return fmt.Sprintf("%s: %v", e.Message, e.Err)
}

// FetchSentimentAnalysis calls the sentiment analysis API.
//
// It sends the given text to the API endpoint and returns a SentimentResponse containing
// the sentiment label and confidence score. If the request fails, it returns an error.
//
// Parameters:
//   - apiURL: The API endpoint for sentiment analysis
//   - text: the input text to be analyzed.
//
// Returns:
//   - A pointer to SentimentResponse containing the label and confidence score.
//   - An error if the request fails or the API response is invalid.
func FetchSentimentAnalysis(apiURL, text string) (*SentimentResponse, error) {
	if text == "" {
		return nil, &APIError{"Invalid input", fmt.Errorf("input cannot be empty")}
	}

	postBody, err := json.Marshal(map[string]string{"text": text})
	if err != nil {
		return nil, &APIError{"Failed to create request payload", err}
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		apiURL,
		bytes.NewBuffer(postBody),
	)
	if err != nil {
		return nil, &APIError{"Failed to create request", err}
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, &APIError{"API request failed", err}
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, &APIError{"API returned non-200 status", fmt.Errorf("status: %d", resp.StatusCode)}
	}

	var modelResponse SentimentResponse
	if err := json.NewDecoder(resp.Body).Decode(&modelResponse); err != nil {
		return nil, &APIError{"Failed to parse response", err}
	}

	return &modelResponse, nil
}
