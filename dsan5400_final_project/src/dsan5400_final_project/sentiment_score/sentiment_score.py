import os
import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging

class SentimentAnalysis:
    def __init__(self):
        # Set current working directory to py directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # logging setting
        logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

    
        self.paths = {
            'RT Audiences': '../../../data/audiences_reviews.csv',
            'RT Critics': '../../../data/critics_reviews.csv',
            'IMDb': '../../../data/imdb_reviews.csv'
        }

        nltk.download('vader_lexicon')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.sia = SentimentIntensityAnalyzer()
        logging.info("SentimentAnalysis instance created and NLTK resources downloaded.")

    def process_reviews(self, data_path):
        """ Process movie reviews from a CSV file. """
        data = pd.read_csv(data_path)
        logging.info(f"Data loaded from {data_path}")

        data.drop_duplicates(inplace=True)
        data.dropna(inplace=True)
        logging.info("Duplicates and missing data removed.")

        columns_to_drop = ['Date', 'Oscar Won', 'year']
        data.drop(columns=[col for col in columns_to_drop if col in data.columns], inplace=True)
        logging.info("Unnecessary columns dropped.")

        column_map = {'title': 'Name', 'Movie Name': 'Name', 'reviewText': 'Review'}
        data.rename(columns=column_map, inplace=True)
        data = data[['Name', 'Review']] if 'Review' in data.columns else data
        logging.info("Columns selected and renamed.")
        return data

    def clean_text(self, text):
        """ Clean text by removing unwanted characters and normalizing whitespaces. """
        text = re.sub(r'@[\w]*', '', text)
        text = re.sub(r'#[\w]*', '', text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'www\S+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        logging.info("Text cleaned.")
        return text

    def analyze_sentiment(self, text):
        """ Analyze sentiment using NLTK's VADER. """
        score = self.sia.polarity_scores(text)
        logging.debug(f"Sentiment analysis completed for text: {text[:60]}...")
        return score['compound']

    def average_scores_from_sources(self, movie_name):
        """ Calculate average sentiment scores for a movie from multiple sources. """
        scores = {}
        for source_name, path in self.paths.items():
            data = self.process_reviews(path)
            data['Review'] = data['Review'].apply(self.clean_text)
            data['Sentiment'] = data['Review'].apply(self.analyze_sentiment)
            if movie_name in data['Name'].unique():
                scores[source_name] = data[data['Name'] == movie_name]['Sentiment'].mean()
            else:
                scores[source_name] = f"No data available for movie: {movie_name} in {source_name}"
            logging.info(f"Average score for '{movie_name}' from {source_name}: {scores[source_name]}")
        return scores

# Use Case
if __name__ == "__main__":
    analyzer = SentimentAnalysis()
    movie_name = 'Oppenheimer'
    scores = analyzer.average_scores_from_sources(movie_name)
    for source, score in scores.items():
        print(f"{source} Average Score: {score}")
