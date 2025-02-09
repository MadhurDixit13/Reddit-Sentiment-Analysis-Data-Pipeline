import streamlit as st
import pandas as pd
import plotly.express as px
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get AWS Credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def get_latest_parquet_file():
    """Fetch the latest Parquet file from S3 by last modified timestamp."""
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        if 'Contents' not in response:
            st.warning("No files found in the S3 bucket.")
            return None

        # Filter only parquet files and sort by LastModified
        parquet_files = [obj for obj in response['Contents'] if obj['Key'].endswith('.parquet')]
        if not parquet_files:
            st.warning("No Parquet files found in the S3 bucket.")
            return None
        
        latest_file = max(parquet_files, key=lambda x: x['LastModified'])
        return latest_file['Key']
    
    except Exception as e:
        st.error(f"Error fetching latest file from S3: {e}")
        return None

def download_from_s3():
    """Download the latest Parquet file from S3 and load it into a DataFrame."""
    latest_file = get_latest_parquet_file()
    if not latest_file:
        return pd.DataFrame()  # Return empty DataFrame if no file found

    local_file_path = f"/tmp/{latest_file}"
    
    try:
        s3.download_file(S3_BUCKET_NAME, latest_file, local_file_path)
        df = pd.read_parquet(local_file_path)
        return df
    except Exception as e:
        st.error(f"Error downloading file from S3: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("📊 Reddit Data Dashboard")
st.write("This dashboard visualizes sentiment analysis of Reddit posts.")

# Load data
df = download_from_s3()

if not df.empty:
    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.write(df)

    # Top subreddits by number of posts
    subreddit_count = df["subreddit"].value_counts().reset_index()
    subreddit_count.columns = ["Subreddit", "Number of Posts"]

    fig1 = px.bar(subreddit_count, x="Subreddit", y="Number of Posts", title="Top Subreddits by Number of Posts")
    st.plotly_chart(fig1)

    # Sentiment distribution
    fig2 = px.histogram(df, x="sentiment_score", title="Sentiment Score Distribution", nbins=20)
    st.plotly_chart(fig2)

    # Average sentiment per subreddit
    sentiment_per_subreddit = df.groupby("subreddit")["sentiment_score"].mean().reset_index()
    fig3 = px.bar(sentiment_per_subreddit, x="subreddit", y="sentiment_score", title="Average Sentiment per Subreddit")
    st.plotly_chart(fig3)

else:
    st.warning("No data available. Please check if the S3 bucket contains the latest dataset.")

st.sidebar.write("Developed by **Madhur Dixit**")
