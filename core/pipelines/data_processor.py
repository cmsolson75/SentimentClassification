import torch
from typing import Callable
import numpy as np


class DataProcessingPipeline:
    SEQUENCE_LENGTH = 256
    SPECIAL_TOKENS = ["<PAD>"]

    def __init__(self, vocab_path: str, data_processer: Callable):
        self.stoi = self.load_vocab(vocab_path)
        self.data_processer = data_processer

    def load_vocab(self, path) -> list:
        with open(path) as f:
            vocab = [line.strip() for line in f.readlines()]

        word2int = {word: idx for idx, word in enumerate(self.SPECIAL_TOKENS + vocab)}
        return word2int

    def encode_text(self, text):
        output = []
        for word in text.split():
            try:
                output.append(self.stoi[word])
            except:
                continue
        return output

    def pad_features(self, reviews, pad_id, seq_length=128):
        features = np.full((len(reviews), seq_length), pad_id, dtype=int)

        for i, row in enumerate(reviews):
            features[i, : len(row)] = np.array(row)[:seq_length]
        return features

    def process(self, text: str) -> torch.Tensor:
        encoded_text = [self.encode_text(self.data_processer(text))]
        return torch.from_numpy(
            self.pad_features(
                encoded_text, pad_id=self.stoi["<PAD>"], seq_length=self.SEQUENCE_LENGTH
            )
        )