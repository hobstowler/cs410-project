import os.path
import argparse

from loader import Loader

models = {
    'base': None,
    'product-base': 'defex/distilgpt2-finetuned-amazon-reviews',
    'amazon-fine-tune': 'LiYuan/amazon-review-sentiment-analysis'
}

def init(args):
    raw_dir = os.path.join(os.getcwd(), 'raw')
    processed_dir = os.path.join(os.getcwd(), 'processed')

    if not os.path.exists(raw_dir):
        print('Directory "raw" does not exist. Creating it...')
        os.mkdir(raw_dir)

    if not os.path.exists(processed_dir):
        print('Directory "processed" does not exist. Creating it...')
        os.mkdir(processed_dir)

def load(args):
    print(f"Loading data from {args.file}.")
    filepath = os.path.join(os.getcwd(), 'raw', args.file)
    _, processed_filepath = Loader.load(filepath, args.keys.split(','))

    if args.run:
        _run_sentiment_analysis(processed_filepath)

def run(args):
    print("Running the sentiment analysis...")


def _run_sentiment_analysis(filepath):
    pass


def list_available_data_sets():
    raw_dir = os.path.join(os.getcwd(), 'raw')
    if os.path.exists(raw_dir):
        print('Available data sets:')
        for w in os.listdir(raw_dir):
            print(f'\t{w}')

        print('\nDownload additional data sets from https://amazon-reviews-2023.github.io')
    else:
        raise FileNotFoundError(
            'Raw directory not found. The `raw` directory must be present at the top level of the project.')

def list_available_models():
    pass

# Create the main parser
def main():
    parser = argparse.ArgumentParser(description="A program that can load Amazon user review data sets, process, and run sentiment analysis on the text of the review.")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    init_parser = subparsers.add_parser('init', help='Initialize the directories.')
    init_parser.set_defaults(func=init)

    load_parser = subparsers.add_parser('load', help="Load the selected data set.")
    load_parser.add_argument('-f', '--file', type=str, help="The data file to load from the raw directory. Use the list command to see available data sets.", required=True)
    load_parser.add_argument('-k', '--keys', type=str, help="Valid keys from the source data separated by commas.", default='rating,text,timestamp,verified_purchase,images')
    load_parser.add_argument('-r', '--run', action='store_true', help="Run the sentiment analysis after processing the file.")
    load_parser.set_defaults(func=load)

    run_parser = subparsers.add_parser('run', help="Run sentiment analysis on the processed file.")
    run_parser.add_argument('-f', '--file', type=str, help="The processed file from the load command.", required=False)
    run_parser.set_defaults(func=run)

    list_parser = subparsers.add_parser('list', help="List the available data sets in the 'raw' directory.")
    list_parser.set_defaults(func=list_available_data_sets)

    models_list_parser = subparsers.add_parser('models', help="List the available models.")
    models_list_parser.set_defaults(func=list_available_models)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
