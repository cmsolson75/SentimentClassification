FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt ./

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]