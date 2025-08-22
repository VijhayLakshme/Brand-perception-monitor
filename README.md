# **Brand-Perception-Monitor**

📰 Brand Perception Monitor is an interactive Streamlit dashboard for analyzing brand perception across YouTube, Reddit, and News platforms. The tool collects and processes comments/posts, applies NLP-based sentiment analysis, and visualizes brand trends to provide actionable insights for businesses. Designed for easy navigation, with separate views for each platform and clickable links for reference.

📁 Features

✅ Multi-platform data integration:

YouTube comments

Reddit posts

News articles

✅ Sentiment Analysis (Positive, Negative, Neutral) using NLP
✅ Trend Tracking of mentions over time
✅ Keyword Extraction for identifying discussion themes
✅ Platform-Specific Tabs for easy navigation
✅ Interactive Visualizations with Plotly & Seaborn
✅ Clickable Links to original posts/articles

📦 Tech Stack

-Python 3.x
-Streamlit (Dashboard)
-NLTK / spaCy / TextBlob (Sentiment Analysis)
-Pandas, NumPy (Data Handling)
-Matplotlib, Seaborn, Plotly (Visualizations)
-APIs / Scrapers for YouTube, Reddit, and News data

🚀 How to Run
Clone the repository
git clone https://github.com/yourusername/brand-perception-monitor.git  
cd brand-perception-monitor  

Install required packages
pip install -r requirements.txt  

Run the Streamlit app
streamlit run brand_monitor.py  

📂 Dataset Format

-YouTube: Video ID → fetches comments
-Reddit: Subreddit/topic → fetches posts & comments
-News: Keywords → fetches latest articles
-Columns include: text, date, source, sentiment

🎯 Use Case

Designed for businesses and product teams to track how their brand is being perceived online, identify sentiment trends, and make data-driven marketing and engagement decisions.
