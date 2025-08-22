# fetch_blogs.py

import feedparser
import pandas as pd
import re
from datetime import datetime
from urllib.parse import quote
import html
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from brand_terms import filter_by_brand_terms

# Setup
nltk.download('vader_lexicon', quiet=True)
sid = SentimentIntensityAnalyzer()

# Sentiment scoring logic
def get_sentiment(text):
    score = sid.polarity_scores(str(text))['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Clean HTML from summaries
def clean_html(raw_html):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html.unescape(raw_html)).strip()

# Main blog scraping function
def scrape_blogs(query="LeapScholar", max_articles=50):
    rss_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={rss_query}"

    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:max_articles]:
        try:
            title = html.unescape(entry.title)
            link = entry.link
            published_raw = entry.published if 'published' in entry else str(datetime.now())
            published = datetime.strptime(published_raw, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
            summary_raw = entry.summary if 'summary' in entry else ""
            summary_clean = clean_html(summary_raw)[:400]

            articles.append([published, title, summary_clean, "Blog", link])
        except Exception as e:
            print(f"[Error Skipping Entry] {e}")
            continue

    # Convert to DataFrame
    if articles:
        df = pd.DataFrame(articles, columns=["Date", "User", "Text", "Source", "URL"])
        df['Sentiment'] = df['Text'].apply(get_sentiment)
        df = filter_by_brand_terms(df, column='Text')  # Now safe to apply
    else:
        df = pd.DataFrame(columns=["Date", "User", "Text", "Source", "URL", "Sentiment"])

    return df
