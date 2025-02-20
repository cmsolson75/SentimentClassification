from core.pipelines.data_processor import DataProcessingPipeline
from core.utils import preprocess_text
from core.services.model_service import ModelService
from functools import lru_cache
import spacy
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache()
def create_model_service() -> ModelService:
    """
    Initializes and caches the model service.

    Returns:
        ModelService: Initialize model service instance.
    """
    try:
        model_path = "models/weights/script_lstm.pt"
        vocab_path = "models/weights/vocab.txt"

        # Initializing NLP model from spaCy
        nlp = spacy.load("en_core_web_sm")

        data_processor = DataProcessingPipeline(
            vocab_path=vocab_path, text_processer=preprocess_text, nlp=nlp
        )
        return ModelService(model_path, data_processor)
    except Exception as e:
        logger.error(f"Failed to initialize model service: {e}")
        raise RuntimeError("Model initialization failed") from e
