import gzip
import json
import os


class Loader:
    @staticmethod
    def load(filepath: str, keys: list = None):
        if keys is None:
            keys = ['rating', 'text', 'timestamp', 'verified_purchase', 'images']

        filename = filepath.split('/')[-1].split('.')[0]
        new_filepath = os.path.join(os.getcwd(), 'processed', f'{filename}.json')

        data = []

        with gzip.open(filepath, 'rb') as f:
            for line in f:
                item = {k: v for k, v in json.loads(line).items() if k in keys}

                if item.get('image') is not None:
                    item.pop('image')
                    item['has_images'] = 1 if len(item['image']) > 0 else 0

                data.append(item)

        with open(new_filepath, 'wb') as f:
            json.dump(data, f)

        return data, new_filepath


if __name__ == '__main__':
    loader = Loader()
    loader.load(os.path.join(os.getcwd(), 'raw', 'Digital_Music.jsonl.gz'))