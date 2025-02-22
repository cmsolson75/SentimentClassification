# Sentiment Analysis with LSTM, FastAPI, and BubbleTea

## Overview

This project is an educational demonstration of deploying a sentiment analysis model using **PyTorch (TorchScript)**, **FastAPI**, and **GoLang (BubbleTea)** for the interface. It aims to teach how to preprocess data, deploy machine learning models, containerize applications, and build a full pipeline for model inference.

## Features

- **Machine Learning Model**: Uses an LSTM model trained in **PyTorch** and exported with **TorchScript**.
- **Data Processing**: Implements preprocessing and tokenization with **spaCy** and custom processing functions.
- **API Deployment**: The model is served through a **FastAPI** backend.
- **TUI Interface**: A lightweight **GoLang** text-based UI (TUI) built using **BubbleTea**.
- **Containerized Application**: The entire application runs with **Docker Compose**.
- **End-to-End Example**: Covers data preprocessing, model inference, and API integration.

## Project Structure

```
.
├── README.md
├── app                # GoLang TUI Interface
│   ├── Dockerfile
│   ├── api.go
│   ├── config.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   ├── tui.go
├── server             # FastAPI Backend for Model Inference
│   ├── Dockerfile
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── inference.py
│   │   ├── schemas.py
│   ├── core
│   │   ├── pipelines
│   │   │   ├── __init__.py
│   │   │   ├── data_processor.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── model_service.py
│   │   ├── utils.py
│   ├── main.py
│   ├── models
│   │   ├── architecture
│   │   │   ├── model.py
│   │   │   ├── model_config.yaml
│   │   ├── weights
│   │       ├── script_lstm.pt
│   │       ├── sentiment_lstm.pt
│   │       ├── vocab.txt
│   ├── requirements.txt
│   ├── setup.sh
│   ├── test_api.py
├── docker-compose.yml
```
---

## **Installation & Setup**

### **Option 1: Run with Docker (Recommended)**
This method ensures all dependencies are installed automatically.

#### **Step 1: Install Docker**
If you haven’t installed Docker yet, follow the instructions for your OS:

- **Windows & macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** Follow the official guide for [Docker Engine](https://docs.docker.com/engine/install/)  
  *(Ensure you also install `docker-compose` if it’s not included.)*

#### **Step 2: Build and Run**
Once Docker is installed, open a terminal and run:

```sh
git clone https://github.com/cmsolson75/SentimentClassification.git
cd SentimentClassification
docker compose build
docker compose run app
```

This will:
- Build the necessary Docker containers.
- Start the FastAPI backend.
- Launch the TUI (Text User Interface) in your terminal.

---

### **Option 2: Run Without Docker (Manual Setup)**
If you prefer to run the app manually, you’ll need to set up the environment yourself.

#### **Step 1: Install Python and Go**
- Install **Python 3.10+** from [python.org](https://www.python.org/downloads/)
- Install **Go** from [golang.org](https://golang.org/dl/)

#### **Step 2: Set Up the Backend (FastAPI)**
1. Navigate to the `server` directory:
   ```sh
   cd server
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. Run the FastAPI server:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### **Step 3: Run the TUI (Go Application)**
1. Navigate to the `app` directory:
   ```sh
   cd ../app
   ```
2. Install dependencies:
   ```sh
   go mod tidy
   ```
3. Run the app:
   ```sh
   go run main.go
   ```

---



### 3. API Endpoints

Once running, the **FastAPI** server is accessible at `http://localhost:8000`.

#### **POST /predict**
- **Description**: Returns the sentiment classification of a given text.
- **Request Body**:
  ```json
  {
    "text": "I love this!"
  }
  ```
- **Response**:
  ```json
  {
    "label": "Positive",
    "confidence": 0.98
  }
  ```

## Key Technologies

- **PyTorch / TorchScript** – Model training & inference
- **FastAPI** – REST API framework
- **spaCy** – Tokenization & NLP processing
- **GoLang (BubbleTea)** – TUI implementation
- **Docker / Docker Compose** – Containerization
- **YAML & Shell Scripts** – Deployment automation

## Educational Goals

This project is designed as a **learning resource** for:
- **Building and deploying machine learning models**
- **Preprocessing and cleaning NLP data**
- **Serving models via an API**
- **Building CLI-based UIs with Go**
- **Containerizing applications with Docker**

## Next Steps for Students
Once you have the project running, try extending it with any of these improvements:
- **Deploy to a Cloud Provider:**
    - Deploy the FastAPI backend to **AWS**, **GCP**, or **Azure**.
    - Since the model runs on CPU, no GPU instance is required.
    - Use **Google Cloud Run**, **AWS Lambda**, or an **EC2** instance for hosting. 
    - **The API is already containerized so deployment should be straightforward.**
- **Implement a Request Queue:** 
    - Use Redis + Celery to queue user requests, preventing API overload.
    - This will help scale the system for higher traffic.
- **Swap the LSTM Model with a Transformer:**
    - Replace the current model with a HuggingFace Transformer (e.g., distilbert-base-uncased).
    - Update the preprocessing pipeline to handle tokenization for transformers.
    - NOTE: This might require you to deploy with a GPU.