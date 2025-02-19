# This is cross cutting so it could go in a different layer
from core.pipelines.data_processor import DataProcessingPipeline
from core.utils import preprocess_pipeline
from core.services.model_service import ModelService
from functools import lru_cache

@lru_cache()
def create_model_service() -> ModelService:
    model_path = "models/weights/script_lstm.pt"
    vocab_path = "models/weights/vocab.txt"
    data_processor = DataProcessingPipeline(vocab_path=vocab_path, data_processer=preprocess_pipeline)
    return ModelService(model_path, vocab_path, data_processor)