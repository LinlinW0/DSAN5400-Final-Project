import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging
from sentiment_score import SentimentAnalysis 

class SentimentComparison(SentimentAnalysis):
    def compare_sentiment_before_after(self, movie_name, event_date):
        """ Compare sentiment before and after a specific event date. """
        before_after_scores = {}
        for source_name, path in self.paths.items():
            data = self.process_reviews(path)
            data['Review'] = data['Review'].apply(self.clean_text)
            data['Sentiment'] = data['Review'].apply(self.analyze_sentiment)
            data['Date'] = pd.to_datetime(data['Date'])

            before_data = data[data['Date'] < pd.Timestamp(event_date)]
            after_data = data[data['Date'] >= pd.Timestamp(event_date)]

            if movie_name in data['Name'].unique():
                before_score = before_data[before_data['Name'] == movie_name]['Sentiment'].mean()
                after_score = after_data[after_data['Name'] == movie_name]['Sentiment'].mean()
                before_after_scores[source_name] = {
                    'Before': before_score,
                    'After': after_score
                }
            else:
                before_after_scores[source_name] = "No data available for movie"

            logging.info(f"Sentiment comparison for '{movie_name}' from {source_name}: Before {before_score}, After {after_score}")
        return before_after_scores

if __name__ == "__main__":
    comparison = SentimentComparison()
    movie_name = 'Oppenheimer'
    event_date = '2023-07-21'
    scores = comparison.compare_sentiment_before_after(movie_name, event_date)
    for source, score in scores.items():
        print(f"{source} - Before: {score['Before']}, After: {score['After']}")
