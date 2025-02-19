# This is where the API goes for inference/predict
from fastapi import APIRouter, Depends
from .schemas import InferenceRequest, InferenceResponse
from .dependencies import create_model_service
from core.services.model_service import ModelService


router = APIRouter()

@router.post("/predict", response_model=InferenceResponse)
async def predict(request: InferenceRequest, model_service: ModelService = Depends(create_model_service)):
    pred = model_service.predict(request.text)
    return InferenceResponse(text=pred)
