import torch
from core.pipelines.data_processor import DataProcessingPipeline


class ModelService:
    def __init__(self, model_path: str, vocab_path: str, data_processing_pipeline: DataProcessingPipeline):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.jit.load(model_path, map_location=torch.device(device))
        self.pre_process = data_processing_pipeline
        self.model.eval()


    def predict(self, text):
        text_tensor = self.pre_process.process(text)
        with torch.no_grad():
            output = "Positive" if self.model(text_tensor).item() >= 0.5 else "Negative"
        return output
