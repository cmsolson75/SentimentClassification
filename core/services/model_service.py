import torch
from core.pipelines.data_processor import DataProcessingPipeline
from typing import Tuple


class ModelService:
    """Service for loading a TorchScript model and making predictions."""

    def __init__(
        self,
        model_path: str,
        data_processing_pipeline: DataProcessingPipeline,
    ):
        """
        Initialize the model service.

        Args:
            model_path (str): Path to the serialized PyTorch model.
            data_processing_pipeline (DataProcessingPipeline): Preprocessing pipeline for text input.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.pre_process = data_processing_pipeline
        self.model.eval()

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict sentiment for a single text input and return both the label confidece score.

        Args:
            text (str): Input text to classify.

        Returns:
            Tuple[str, float]: Sentiment label ("Positive" or "Negative") and confidence score (0 to 1).
        """
        try:
            text_tensor = self.pre_process.process(text).to(self.device)

            with torch.no_grad():
                prediction = self.model(text_tensor).item()

            label = "Positive" if prediction >= 0.5 else "Negative"

            confidence = abs(prediction - 0.5) * 2

            return label, confidence
        except Exception as e:
            return f"Prediction failed: {str(e)}", -1
