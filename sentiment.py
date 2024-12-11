import json
import os
import random

import torch.cuda
import numpy as np

from torch.utils.hipify.hipify_python import InputError
from transformers import pipeline
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    hugging_face = False
    text_blob = False
    vader = False

    def __init__(self, filepath: str, sample_size=10000, hugging_face: any = False, text_blob=False, vader=False, device=None):
        if not hugging_face and not text_blob and not vader:
            raise InputError('Model not specified')

        if hugging_face:
            self.hugging_face = hugging_face
            if device is None:
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                print(f'Using {device}.')

            try:
                self.pipeline = pipeline('sentiment-analysis', model=hugging_face, device=device, truncation=True)
            except AssertionError as e:
                print(e)
                print(f'Using cpu instead.')
                self.pipeline = pipeline('sentiment-analysis', model=hugging_face, device='cpu', truncation=True)
        elif text_blob:
            self.text_blob = text_blob
            self.model_name = 'textblob'
        elif vader:
            self.vader = vader
            self.model_name = 'vader'

        self.filepath = filepath
        self.sample_size = sample_size

    def run(self):
        # load the file and sample a subset of data
        sample_data = self._load_file()

        # retrieve just the text for analysis
        text = self._get_text(sample_data)

        # run the analysis
        print('Running sentiment analysis...', end='')
        sentiment = self._analyze_sentiment(text)
        combined_data = [{**z1, **z2} for z1, z2 in zip(sample_data, sentiment)]
        print('Done.')

        # sort into buckets based on rating
        print('Sorting results into buckets based on given rating...', end='')
        buckets = self._sort_sentiment_by_rating(combined_data)
        buckets.update({'all': combined_data})
        print('Done.')

        #output intermediate results
        print('Saving intermediate results...', end='')
        basename = os.path.basename(self.filepath)
        filename = os.path.join(os.getcwd(), 'analyzed', f'{basename.split(".")[0]}_{self.model_name.replace("/", "_")}.json')
        self._output_to_file(filename, buckets)

        print('Calculating performance and accuracy...', end='')
        performance = {k: self._calculate_error(k, bucket) for k, bucket in buckets.items()}
        print('Done.')

        print('Saving final results...', end='')
        filename = os.path.join(os.getcwd(), 'analyzed', f'{basename.split(".")[0]}_{self.model_name.replace("/", "_")}_results.json')
        self._output_to_file(filename, performance)

    def _calculate_error(self, actual_score: float, bucket: list):
        scores = np.array(list(b['score'] for b in bucket))
        if actual_score == 'all':
            actual_scores = np.array(list(b['rating'] for b in bucket))
        else:
            actual_scores = np.full(scores.shape, float(actual_score))

        mae = np.mean(np.abs(scores - actual_scores))
        rmse = np.sqrt(np.mean((scores - actual_scores) ** 2))
        acc = np.mean(np.isclose(np.round(scores, 0), actual_scores))

        return {'size': len(bucket), 'mae': round(float(mae), 4), 'rmse': round(float(rmse), 4), 'acc': round(float(acc), 4)}

    def _load_file(self):
        data = json.load(open(self.filepath))

        print(f'Sampling data with sample size of {self.sample_size}.')
        sample_data = random.sample(data, self.sample_size)

        return sample_data

    def _get_text(self, sample_data) -> list:
        return [review.get('text', '') for review in sample_data]

    def _analyze_sentiment(self, text: list):
        if self.hugging_face:
            return self.pipeline(text)
        elif self.text_blob:
            sentiment = []
            for review in text:
                score = (TextBlob(review).sentiment.polarity + 1) / 2 * 5
                if score < 2.5:
                    label = 'NEGATIVE'
                elif score > 2.5:
                    label = 'POSITIVE'
                else:
                    label = 'NEUTRAL'
                sentiment.append({'score': score, 'label': label})
            return sentiment
        elif self.vader:
            sentiment = []
            analyzer = SentimentIntensityAnalyzer()
            for review in text:
                score = (analyzer.polarity_scores(review)['compound'] + 1) / 2 * 5
                if score < 2.5:
                    label = 'NEGATIVE'
                elif score > 2.5:
                    label = 'POSITIVE'
                else:
                    label = 'NEUTRAL'
                sentiment.append({'score': score, 'label': label})
            return sentiment

    def _sort_sentiment_by_rating(self, combined_data):
        buckets = {1.0: [], 2.0: [], 3.0: [], 4.0: [], 5.0: []}

        for review in combined_data:
            buckets[review['rating']].append({k: v for k, v in review.items() if k not in ['rating', 'text']})

        return buckets

    def _output_to_file(self, filename, buckets):
        with open(filename, 'w') as f:
            json.dump(buckets, f)

        print(f'Output stored at {filename}')


if __name__ == '__main__':
    # data = json.load(open(r'processed\Digital_Music.json'))
    # s = SentimentAnalyzer(file_name='Digital_Music.json', hugging_face='siebert/sentiment-roberta-large-english', device='cuda')
    s = SentimentAnalyzer(filepath='Digital_Music.json', text_blob=True, device='cuda')
    # s = SentimentAnalyzer(file_name='Digital_Music.json', vader=True, device='cuda')
    s.run()
    # analyzer = SentimentIntensityAnalyzer()
    # print(analyzer.polarity_scores("If i had a dollar for how many times I have played this cd and how many times I have asked Alexa to play it, I would be rich. Love this singer along with the Black Pumas. Finding a lot of new music that I like a lot on amazon. Try new things."))
