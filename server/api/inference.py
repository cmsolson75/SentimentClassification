# This is where the API goes for inference/predict
from fastapi import APIRouter, Depends, HTTPException
from .schemas import InferenceRequest, InferenceResponse
from .dependencies import create_model_service
from core.services.model_service import ModelService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/predict", response_model=InferenceResponse)
async def predict(
    request: InferenceRequest,
    model_service: ModelService = Depends(create_model_service),
):
    """
    Predict sentiment of input text using the model service

    Args:
        request (InferenceRequest): JSON request body containing input text.
        model_service (ModelService): Model service instance (injected)

    Returns:
        InferenceResponse: JSON response with predicted label and confidence score. 
    """
    try:
        print(request.text)
        label, confidence = model_service.predict(request.text)
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")
    
    return InferenceResponse(label=label, confidence=confidence)
