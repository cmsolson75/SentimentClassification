import torch
from typing import Callable, Dict
import numpy as np
import spacy


class DataProcessingPipeline:
    """Preprocess and tokenize text for NLP models."""

    SEQUENCE_LENGTH = 256
    SPECIAL_TOKENS = ["<PAD>"]

    def __init__(
        self,
        vocab_path: str,
        text_processer: Callable[[str, spacy.language.Language], str],
        nlp: spacy.language.Language,
    ):
        """Init pipeline with vocab, text processor, and NLP model"""
        self.stoi: Dict[str, int] = self.load_vocab(vocab_path)
        self.text_processer = text_processer
        self.nlp = nlp

    def load_vocab(self, path: str) -> Dict[str, int]:
        """Load vocabulary and create word-to-index mapping"""
        try:
            with open(path) as f:
                vocab = [line.strip() for line in f.readlines()]
            return {word: idx for idx, word in enumerate(self.SPECIAL_TOKENS + vocab)}
        except FileNotFoundError:
            raise ValueError(f"Vocabulary file not found at {path}")

    def encode_text(self, text: str) -> list:
        """Convert text into a list of token IDs, ignoring unknown words."""
        return [self.stoi.get(word) for word in text.split() if word in self.stoi]

    def pad_features(
        self, sequences: list, pad_id: int, seq_length: int = 128
    ) -> np.ndarray:
        """Pad sequences to a fixed length with <PAD> token ID."""
        features = np.full((len(sequences), seq_length), pad_id, dtype=int)

        for i, row in enumerate(sequences):
            row_length = min(len(row), seq_length)
            features[i, :row_length] = row[:row_length]
        return features

    def process(self, text: str) -> torch.Tensor:
        """
        Apply text processing, encoding, and padding to return a tensor/

        Args:
            text (str): Input raw text.

        Returns:
            torch.Tensor: Processed and padded tensor for model input.
        """
        processed_text = self.text_processer(text, self.nlp)
        encoded_text = [self.encode_text(processed_text)]
        padded_text = self.pad_features(
            encoded_text, pad_id=self.stoi["<PAD>"], seq_length=self.SEQUENCE_LENGTH
        )
        return torch.from_numpy(padded_text)
