import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bertopic import BERTopic
import plotly.offline as py

class ReviewData:
    '''
    Taking a look at the relative rankings of the sentiment score of data extracted from 3 different
    review websites.
    Using BERTopic to review data from each website, specifically the distinctive topics of the negative 
    reviews of each year's Oscar nominated movie to understand why audiences' sentiments are negative.
    '''
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.negative_sentiment_df = self.df[self.df['sentiment_label'] == 'Negative']
        self.before_df = self.df[self.df['before_after'] == 'before']
        self.average_sentiment_score = self.before_df.groupby(['Year', 'Movie Name', 'Oscar Won'])['sentiment_score'].mean().reset_index()
        self.negative_review_counts = self.negative_sentiment_df.groupby('Movie Name').size().reset_index(name='Negative Review Count')
        self.model = None

    def plot_sentiment_by_year(self, title):
        years = self.average_sentiment_score['Year'].unique()
        years.sort()
        n_subplots = len(years)
        
        fig, axes = plt.subplots(n_subplots, 1, figsize=(10, n_subplots*5), sharex=True)

        for i, year in enumerate(years):
            df_year = self.average_sentiment_score[self.average_sentiment_score['Year'] == year]
            df_year_sorted = df_year.sort_values('sentiment_score', ascending=False)
            sns.barplot(x='sentiment_score', y='Movie Name', data=df_year_sorted, 
                        ax=axes[i], palette=['red' if (x == 'Yes' or x == 'winner') else 'blue' for x in df_year_sorted['Oscar Won']])
            axes[i].set_title(f'{title} - Year: {year}')
            axes[i].set_xlabel('Average Sentiment Score')
            axes[i].set_ylabel('Movie Name')

        plt.tight_layout()
        plt.show()

    def get_topics(self, movie_name):
        reviews = self.negative_sentiment_df[self.negative_sentiment_df['Movie Name'] == movie_name]['Review'].tolist()
        if reviews:
            self.model = BERTopic()
            topics, probabilities = self.model.fit_transform(reviews)
            return topics
        else:
            return None

    def visualize_topics(self):
        if self.model:
            self.model.visualize_hierarchy()
            self.model.visualize_barchart(top_n_topics=5)
            n_topics = len(set(self.model.get_topics()))
            for topic_num in range(n_topics):
                if topic_num == -1:
                    continue
                topic_info = self.model.get_topic(topic_num)
                if topic_info is not None and isinstance(topic_info, list):
                    print(f"Topic {topic_num}: ", [word for word, _ in topic_info])
                else:
                    print("No words associated or topic is an outlier.")



class IMDbReviewData(ReviewData):
    '''Inherit from ReviewData superclass to further process data from IMDb'''
    pass

class RTCriticsReviewData(ReviewData):
    '''Inherit from ReviewData superclass to further process data from Rotten Tomatoes Critics'''
    pass

class RTAudienceReviewData(ReviewData):
    '''Inherit from ReviewData superclass to further process data from Rotten Tomatoes Audience'''
    pass


# Process each dataset using a for loop
datasets = {
    'IMDb': 'Downloads/5400_final_data/imdb.csv',
    'Rotten Tomatoes Critics': 'Downloads/5400_final_data/critics_review.csv',
    'Rotten Tomatoes Audience': 'Downloads/5400_final_data/audience_review.csv'
}

for dataset, path in datasets.items():
    if dataset == 'IMDb':
        data = IMDbReviewData(path)
    elif dataset == 'Rotten Tomatoes Critics':
        data = RTCriticsReviewData(path)
    elif dataset == 'Rotten Tomatoes Audience':
        data = RTAudienceReviewData(path)

    data.plot_sentiment_by_year(f'{dataset} Sentiment Score')
    negative_reviews = data.negative_review_counts.sort_values(by='Negative Review Count', ascending=False).head(10)
    print(f"\nTop 10 movies with the most negative reviews in {dataset}:")
    print(negative_reviews)

    # Get topics and visualize example movies from the IMDb dataset
    if dataset == 'IMDb': # Example review site
        movie_name = "Don't Look Up"  # Example movie from the IMDb dataset
        topics = data.get_topics(movie_name)
        if topics:
            print(f"\nTopics for the movie '{movie_name}':")
            data.visualize_topics()
        else:
            print(f"\nNo negative reviews found for the movie '{movie_name}' in the IMDb dataset.")
