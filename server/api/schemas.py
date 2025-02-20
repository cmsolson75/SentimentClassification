# this is where pydantic models go
from pydantic import BaseModel


class InferenceRequest(BaseModel):
    text: str


class InferenceResponse(BaseModel):
    label: str
    confidence: float
