# fetch_youtube.py
import os
import pandas as pd
from googleapiclient.discovery import build
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from brand_terms import filter_by_brand_terms

# Load environment variables
load_dotenv()
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_sentiment(text):
    score = sid.polarity_scores(str(text))['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def scrape_youtube(keyword="LeapScholar", max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    search_response = youtube.search().list(
        q=keyword, type="video", part="id", maxResults=max_results
    ).execute()

    video_ids = [
        item.get("id", {}).get("videoId")
        for item in search_response.get("items", [])
        if item.get("id", {}).get("videoId")
    ]

    comments = []
    for vid in video_ids:
        try:
            response = youtube.commentThreads().list(
                part="snippet", videoId=vid, textFormat="plainText", maxResults=100
            ).execute()
            for item in response.get("items", []):
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append([
                    comment['publishedAt'],
                    comment['authorDisplayName'],
                    comment['textDisplay'],
                    f"https://www.youtube.com/watch?v={vid}",
                    "YouTube"
                ])
        except Exception as e:
            print(f"Skipping video {vid} due to error: {e}")
            continue

    if comments:
        df = pd.DataFrame(comments, columns=["Date", "User", "Text", "URL", "Source"])
        df['Sentiment'] = df['Text'].apply(get_sentiment)
        df = filter_by_brand_terms(df, column='Text')
    else:
        df = pd.DataFrame(columns=["Date", "User", "Text", "URL", "Source", "Sentiment"])

    return df
