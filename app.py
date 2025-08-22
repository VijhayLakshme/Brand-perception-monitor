import streamlit as st
import pandas as pd
from reddit_scraper import scrape_reddit
from fetch_youtube import scrape_youtube
from fetch_news import scrape_news
from fetch_blogs import scrape_blogs
from brand_terms import filter_by_brand_terms


st.set_page_config(page_title="Leap Brand Monitor", layout="wide")

def format_sentiment(s):
    return "✅ Positive" if s == "Positive" else "⚠️ Negative" if s == "Negative" else "ℹ️ Neutral"

st.title("📊 Leap Brand Visibility Monitor")
st.markdown("Enter a topic Leap is mentioned in the conversation.")

search_term = st.text_input("Enter topic to analyze:", value="IELTS")

if st.button("Search"):
    with st.spinner("Scraping data from Reddit, YouTube, News, and Blogs..."):
        df_reddit_raw = scrape_reddit(search_term, limit=20)
        df_youtube_raw = scrape_youtube(search_term, max_results=5)
        df_news_raw = scrape_news(search_term)
        df_blogs_raw = scrape_blogs(query=search_term.split()[0])  # clean for RSS

        df_reddit = filter_by_brand_terms(df_reddit_raw, column='Text')
        df_youtube = filter_by_brand_terms(df_youtube_raw, column='Text')
        df_news = filter_by_brand_terms(df_news_raw, column='Text')
        df_blogs = filter_by_brand_terms(df_blogs_raw, column='Text')

    total = len(df_reddit) + len(df_youtube) + len(df_news) + len(df_blogs)
    st.success(f"Found {total} Leap mentions related to '{search_term}'")

    tab1, tab2, tab3, tab4 = st.tabs(["Reddit", "YouTube", "News", "Blogs/Web"])

    with tab1:
        st.header("🔴 Reddit")
        if df_reddit.empty:
            st.info("No Leap mentions found on Reddit.")
        else:
            for _, row in df_reddit.iterrows():
                with st.expander(f"{row['Title']} (r/{row['Subreddit']})"):
                    st.markdown(row['Text'][:500])
                    st.markdown(f"{format_sentiment(row['Sentiment'])} | [Open Post]({row['URL']})")

    with tab2:
        st.header("📺 YouTube")
        if df_youtube.empty:
            st.info("No Leap mentions found on YouTube.")
        else:
            for _, row in df_youtube.iterrows():
                with st.expander(f"{row['User']} commented:"):
                    st.markdown(row['Text'][:500])
                    st.markdown(f"{format_sentiment(row['Sentiment'])} | [Watch Video]({row['URL']})")

    with tab3:
        st.header("📰 News Articles")
        if df_news.empty:
            st.info("No Leap mentions found in News.")
        else:
            for _, row in df_news.iterrows():
                with st.expander(f"{row['User']} ({row['Date']})"):
                    st.markdown(f"**Summary:** {row['Text']}")
                    st.markdown(f"**Sentiment:** {format_sentiment(row['Sentiment'])}")
                    st.markdown(f"[🔗 Read Article]({row['URL']})")

    with tab4:
        st.header("📝 Blog/Web Mentions")
        if df_blogs.empty:
            st.info("No Leap mentions found in blogs or web results.")
        else:
            for _, row in df_blogs.iterrows():
                with st.expander(f"{row['User']} ({row['Date']})"):
                    st.markdown(f"**Summary:** {row['Text']}")
                    st.markdown(f"**Sentiment:** {format_sentiment(row['Sentiment'])}")
                    st.markdown(f"[🔗 Read Article]({row['URL']})")
