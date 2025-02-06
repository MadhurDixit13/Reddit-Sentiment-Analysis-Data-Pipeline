import streamlit as st
import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )

@st.cache_data  
def load_data():
    file_name = f"reddit_data_202502060619.parquet"
    s3.download_file("redditpipeline", file_name, file_name)
    df = pd.read_parquet(file_name)
    return df

df = load_data()

st.title("📊 Reddit Sentiment Dashboard")
st.write(df)
st.bar_chart(df.groupby("subreddit")["sentiment_score"].mean())
