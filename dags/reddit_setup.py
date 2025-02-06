from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import praw
import pandas as pd
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()

# Reddit API Credentials
# REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
# REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
# REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
SUBREDDITS = ["anime", "naruto", "soccer", "videogames"]

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def fetch_reddit_data():
    """Fetch top posts from Reddit."""
    all_data = []
    reddit = praw.Reddit(
        client_id=Variable.get("REDDIT_CLIENT_ID"),
        client_secret=Variable.get("REDDIT_CLIENT_SECRET"),
        user_agent=Variable.get("REDDIT_USER_AGENT"),
        username = Variable.get("REDDIT_USERNAME"),
        # password= Variable.get("REDDIT_PASSWORD")
    )
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
    
    # for post in subreddit.hot(limit=10):
    #     print(post)
    #     posts.append({
    #         "title": post.title,
    #         "score": post.score,
    #         "url": post.url,
    #         "created_utc": post.created_utc
    #     })
    
    # df = pd.DataFrame(posts)
    file_name = f"reddit_data_{datetime.now().strftime('%Y%m%d%H%M')}.parquet"
    df.to_parquet(file_name, index=False)
    print("saved") 

def upload_to_s3():
    """Upload CSV file to AWS S3."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Variable.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=Variable.get("AWS_SECRET_KEY")
    )
    file_name = f"reddit_data_{datetime.now().strftime('%Y%m%d%H%M')}.parquet"
    s3.upload_file(file_name, Variable.get("S3_BUCKET_NAME"), file_name)
    print("Uploaded to S3!")



# Define DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1), 
    "retries": 1
}
""" 

Three ways to define a dag 
 1. with statement (context manager), which will add anything inside it to the DAG implicitly:
 with DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 ):
     EmptyOperator(task_id="task")
 2. standard constructor, passing the DAG into any operators you use:
  my_dag = DAG(
     dag_id="my_dag_name",
     start_date=datetime.datetime(2021, 1, 1),
     schedule="@daily",
 )
 EmptyOperator(task_id="task", dag=my_dag)
 3. @dag decorator to turn a function into a DAG generator:
  @dag(start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
  def generate_dag():
     EmptyOperator(task_id="task")
  generate_dag()

  
"""
with DAG(
    "reddit_data_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_reddit_data",
        python_callable=fetch_reddit_data
    )

    upload_task = PythonOperator(
    task_id="upload_to_s3",
    python_callable=upload_to_s3
)

extract_task >> upload_task
