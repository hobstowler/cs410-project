from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, data, model_name=None):
        if model_name is None:
            self.pipeline = pipeline('sentiment-analysis')
        else:
            self.pipeline = pipeline(model=model_name)

        self.raw_data = data

    def run