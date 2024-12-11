# About

This project uses scraped Amazon reviews from 1996 to 2023 collected by [McAuley Lab](https://cseweb.ucsd.edu/~jmcauley/) in 2023. [link](https://amazon-reviews-2023.github.io/)

> **Citation for data sources:**
> 
> **Article**: hou2024bridging
> 
> **Title:** Bridging Language and Items for Retrieval and Recommendation
> 
> **Authors:** Hou, Yupeng and Li, Jiacheng and He, Zhankui and Yan, An and Chen, Xiusi and McAuley, Julian 
> 
> **Journal:** arXiv preprint arXiv:2403.03952
> 
> **Year:** 2024

Using [VADER](https://github.com/cjhutto/vaderSentiment) (Valence Aware Dictionary and sEntiment Reasoner) and [TextBlob](https://textblob.readthedocs.io/) this project attempts to assess the sentiment of the text of Amazon product reviews and evaluate whether the user-provided rating lines up with the sentiment rating.

The success of the models is evaluated based on traditional methods of evaluating language models such as Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE) as well as a measure of the accuracy of the sentiment when compared to the user rating, expressed as a simple percentage of "correct" ratings from the model.

# Instructions

## Installation

1. Install required packages: `pip install requirements.txt`
2. Optional, if you have a cuda supported machine, install torch with cuda: `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
   > See PyTorch install page for other versions: https://pytorch.org/get-started/locally/
 
## Running

### Prerequisites

1. Download a raw dataset from https://amazon-reviews-2023.github.io/
2. Put the downloaded dataset in the `raw` directory in the project.

### Processing Raw Dataset

1. Choose a raw dataset that you previously downloaded in the prerequisite step.
2. Copy the file name and run the following command: `python main.py load -f <RAW_FILE_NAME>`
   > Note: you don't need the full path, just make sure the file is in the `raw` directory
3. Output will be saved to the `processed` directory

### Running Sentiment Analysis

1. Choose a processed file that was output as part of the instructions from the previous section.
2. Copy the file name and run the following command: `python main.py run -f <PROCESSED_FILE_NAME> -m <MODEL_NAME>`
   > Note: you don't need the full path, just make sure the file is in the `processed` directory
   1. Required `-m` parameter can be either `vader` or `textblob` to choose from one of those models for the sentiment analysis.
   2. Optional `-ss` parameter can be used to specify the sample size from the processed data set. Default sample size is 10,000.
3. The program will output intermediate and final results to the `analyzed` folder.
4. Final results will contain information about the accuracy of the sentiment to rating (ACC), the mean absolute error (MAE), and the root mean squared error (RMSE). Sample size for each rating bucket will also be included. 