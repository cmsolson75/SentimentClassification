from fastapi import FastAPI, Depends
from pydantic import BaseModel
from core.pipelines.data_processor import DataProcessingPipeline 
from api.dependencies import create_model_service
from core.services.model_service import ModelService
from api.inference import router as inference_router

model_path = "models/weights/script_lstm.pt"
vocab_path = "models/weights/vocab.txt"


app = FastAPI()
app.include_router(inference_router, tags=["Model Inference"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
