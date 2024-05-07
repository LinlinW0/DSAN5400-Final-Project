# DSAN 5400: Computational Linguistic Final Project

## Topic: Reviews Analysis on Oscar Best Pictures

## Presentation: https://docs.google.com/presentation/d/1QHyylPeI6gZCaMGWRuhWLrI-jgMQAvQVwaRwXh1uxx8/edit?usp=sharing

## Project Description: 

Oscar, as the most prestigious and authoritative movie academy worldwide, appeals movie-lovers’ attention every year. This project, which os also created by 4 movie enthusiastic, analyzed the movie review from different platforms, and the movies are the 47 Oscar Best Picture nominations and winners from the year 2020 to 2024. 

## Project Structure: 

### Data Overview/EDA: 

Script path: dsan5400_final_project/EDA_WordCloud

The data is web-scraped from three sources: IMDB, Rotten Tomato (addressed as RT in the following) Audiences, and Rotten Tomato Critics (TomatoMeter). The first two sources contains movies reviews from all kinds of audience, who are audiences of all kinds of occupations thus not professional movie critics, and vice versa for the TomatoMeter. In total we gathered over 679,000 reviews from those platforms and performed exploratory data analysis using world-cloud: as the minimum frequency of the word increases, there are no sentimental words left for the reviews from Rotten Tomato Critics, and for the other two sources there were “good”, “great”, ect. 

The EDA used one of the template from the the [shinny.oi](https://shiny.posit.co/r/gallery/start-simple/word-cloud/) in R. 

### Sentimental Analysis: 

Script path: dsan5400_final_project/src/dsan5400_final_project/sentiment_score/sentiment_score.py

IMDB audiences have the most positive reviews towards movies in general, follows by RT Audiences, then the RT critics. For each sentiment score distributions for each platform, IMDB reviews have more outliers on the lower end, which are discovered later as “trolls”. 

The SentimentAnalysis class, defined in this script, provides functionality for sentiment analysis on movie reviews sourced from various datasets, using NLTK's VADER sentiment analysis tool. Upon initialization, the class sets the current working directory and configures logging to record operations and statuses throughout the analysis process. It also loads necessary NLTK resources, including the VADER lexicon, tokenizers, and other tools essential for text processing.

The script processes review data stored in CSV files, cleans text to remove extraneous web links, user tags, and other non-relevant characters, and finally applies sentiment analysis. It handles multiple sources of review data such as Rotten Tomatoes audiences and critics reviews, and IMDb reviews, by normalizing column names and dropping irrelevant columns.

For each review, the script performs sentiment analysis to compute a sentiment score. Additionally, it can compute and display the average sentiment score for a specific movie across various data sources, allowing comparisons of sentiment across different platforms and reviewer demographics.

The main execution block of the script creates an instance of SentimentAnalysis, processes the reviews for a specified movie, and prints the average sentiment scores obtained from each data source. This setup is useful for understanding public and critical reception of films based on review sentiment.

### Reviews Before & After the Award Announcement: 

Script Path: dsan5400_final_project/src/dsan5400_final_project/sentiment_score/sentiment_score_before_after.py

The focus shifts to the award winning movie. 

For IMDB reviews, positive reviews remains positive, however, the negative reviews become more negative after the best picture award is announced. The phenomenon could be related to the outliers from the previous section. 

The script SentimentComparison extends the functionality of a SentimentAnalysis class, specifically focusing on comparing the sentiment of movie reviews before and after a specified event date. This specialized subclass is designed to analyze changes in public perception surrounding a movie in relation to a significant event, such as a movie release or a major occurrence related to the film.

Upon initialization, the SentimentComparison class inherits from SentimentAnalysis, leveraging its methods for processing reviews, cleaning text, and analyzing sentiment. The compare_sentiment_before_after method is the core function of this class. It iterates through multiple sources of review data (such as Rotten Tomatoes and IMDb), which are specified in the inherited paths dictionary. For each source, it:

1. Processes the reviews to extract, clean, and analyze sentiment.
2. Converts review dates into datetime format for comparison purposes.
3. Filters the reviews into two groups: those published before and after the specified event date.
4. Calculates the average sentiment scores for reviews of the specified movie in both time periods.
5. Stores these scores in a dictionary, which includes separate entries for sentiment before and after the event, facilitating a direct comparison.

If no data is available for a particular movie in a dataset, it logs and returns a placeholder message indicating the absence of data. The logging functionality, inherited from SentimentAnalysis, provides detailed debug and information logs for each step of the process, aiding in troubleshooting and verification of the workflow.

In the main execution block, an instance of SentimentComparison is created, and the sentiment before and after a specific event date for a given movie is computed and printed. This setup is particularly useful for researchers and analysts interested in studying the impact of external events on public opinion as expressed in film reviews.

### Which platform is more predictive: 

Script Path: 

IMDB audiences are more positive towards the wining movie each year, which we evaluated by aggregating the rank of the wining movie, compares to other nominations each year. 

### Conclusions: 

Sentiment score average ranking: IMDB > RT audience > RT critics. 

After announcing the winner of the best picture, relatively more negative reviews appears on IMDB. 

Reviews from IMDB are more predictable on which movie wins.