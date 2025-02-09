from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import praw
import pandas as pd
from datetime import datetime
import boto3
from dotenv import load_dotenv
from textblob import TextBlob
import logging
import subprocess
import os

load_dotenv()

# Define Subreddits
SUBREDDITS = ["anime", "naruto", "soccer", "videogames"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=Variable.get("REDDIT_CLIENT_ID"),
    client_secret=Variable.get("REDDIT_CLIENT_SECRET"),
    user_agent=Variable.get("REDDIT_USER_AGENT"),
    username=Variable.get("REDDIT_USERNAME"),
)

# Initialize S3 Client
s3 = boto3.client(
        "s3",
        aws_access_key_id=Variable.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=Variable.get("AWS_SECRET_KEY")
    )

def analyze_sentiment(text):
    """Analyze sentiment of a given text using TextBlob."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def fetch_reddit_data(**kwargs):
    """Fetch top posts from Reddit and save them as a Parquet file."""
    all_data = []
    
    for subreddit in SUBREDDITS:
        for post in reddit.subreddit(subreddit).hot(limit=50):
            sentiment_score = analyze_sentiment(post.title)

            all_data.append({
                "subreddit": subreddit,
                "title": post.title,
                "score": post.score,
                "sentiment_score": sentiment_score,
                "num_comments": post.num_comments,
                "url": post.url,
                "created_utc": datetime.utcfromtimestamp(post.created_utc),
            })

    df = pd.DataFrame(all_data)

    # Generate a consistent filename
    file_name = f"reddit_data_{datetime.now().strftime('%Y%m%d%H%M')}.parquet"
    Variable.set("LATEST_REDDIT_FILE", file_name)  # Store filename in Airflow Variable

    df.to_parquet(file_name, index=False)
    logger.info(f"Saved Reddit data to {file_name}")

    # Push filename to XCom for the next task
    kwargs['ti'].xcom_push(key="file_name", value=file_name)

def upload_to_s3(**kwargs):
    """Upload the Parquet file to AWS S3."""
    ti = kwargs['ti']
    file_name = ti.xcom_pull(task_ids='extract_reddit_data', key="file_name")

    bucket_name = Variable.get("S3_BUCKET_NAME")
    try:
        s3.upload_file(file_name, bucket_name, file_name)
        logger.info(f"Uploaded {file_name} to S3 bucket {bucket_name}.")
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")

def load_data_from_s3(**kwargs):
    """Download the latest Reddit data from S3."""
    file_name = Variable.get("LATEST_REDDIT_FILE")
    bucket_name = Variable.get("S3_BUCKET_NAME")

    local_file = f"/tmp/{file_name}"  # Store temporarily

    try:
        s3.download_file(bucket_name, file_name, local_file)
        df = pd.read_parquet(local_file)

        csv_path = "/tmp/reddit_data.csv"
        df.to_csv(csv_path, index=False)  # Save as CSV for Streamlit

        if os.path.exists(csv_path):  # Ensure file exists
            kwargs['ti'].xcom_push(key="csv_file", value=csv_path)
            print(f"✅ Data loaded successfully: {csv_path}")
        else:
            raise FileNotFoundError("❌ CSV file was not created.")

    except Exception as e:
        print(f"⚠️ Error loading data from S3: {e}")
        raise  # Rethrow error so Airflow knows it failed

def generate_dashboard(**kwargs):
    """Generate visualizations from the Reddit dataset."""
    ti = kwargs['ti']
    csv_file = ti.xcom_pull(task_ids='load_data', key="csv_file")

    df = pd.read_csv(csv_file)
    
    # Example visualization: Aggregating sentiment scores
    sentiment_summary = df.groupby("subreddit")["sentiment_score"].mean()
    
    print("📊 Sentiment Score by Subreddit:")
    print(sentiment_summary)

    # Save visualization data
    summary_path = "/tmp/sentiment_summary.csv"
    sentiment_summary.to_csv(summary_path)
    ti.xcom_push(key="summary_file", value=summary_path)

# Define DAG default arguments
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

# Define DAG using 'with' statement
with DAG(
    "reddit_data_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_reddit_data",
        python_callable=fetch_reddit_data,
        provide_context=True
    )

    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data_from_s3,
        provide_context=True
    )

    dashboard_task = PythonOperator(
        task_id="generate_dashboard",
        python_callable=generate_dashboard,
        provide_context=True
    )

# Define DAG execution order
extract_task >> upload_task >> load_task >> dashboard_task
