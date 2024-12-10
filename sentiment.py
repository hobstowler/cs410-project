import torch.cuda
from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, data: dict, model_name=None, device=None):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(device)

        if model_name is None:
            self.pipeline = pipeline('sentiment-analysis', device=device)
        else:
            self.pipeline = pipeline(model=model_name)

        self.raw_data = data

    def run(self):
        print(self._get_text())

    def _get_text(self) -> list:
        return [value for key, value in self.raw_data.items() if key == 'text']


if __name__ == '__main__':
    s = SentimentAnalyzer(None, device='cuda')
    s.run()