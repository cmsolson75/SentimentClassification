from torch import nn
import torch


class SentimentModel(nn.Module):
    def __init__(
        self,
        vocab_size,
        output_size,
        hidden_size=128,
        embedding_size=400,
        n_layers=2,
        dropout=0.2,
    ):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_size)

        self.lstm = nn.LSTM(
            embedding_size, hidden_size, n_layers, dropout=dropout, batch_first=True
        )
        self.dropout = nn.Dropout(0.3)

        self.fc = nn.Linear(hidden_size, output_size)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.long()

        x = self.embedding(x)

        o, _ = self.lstm(x)
        o = o[:, -1, :]

        o = self.dropout(o)
        o = self.fc(o)

        o = self.sigmoid(o)
        return o


def script_model(model_path, output_path):
    import yaml

    with open("model_config.yaml", "r") as file:
        config = yaml.safe_load(file)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = SentimentModel(
        config['vocab_size'],
        config['output_size'],
        config['hidden_size'],
        config['embedding_size'],
        config['n_layers'],
        config['dropout'],
    ).to(device)

    model.load_state_dict(
        torch.load(model_path, map_location=torch.device(device), weights_only=True)
    )

    script = torch.jit.script(model)
    script.save(output_path)

if __name__ == "__main__":
    script_model("/Users/cameronolson/Developer/Personal/Learning/FastAI/projects/SentementClassificationSimple/models/weights/sentiment_lstm.pt", "../test.pt")