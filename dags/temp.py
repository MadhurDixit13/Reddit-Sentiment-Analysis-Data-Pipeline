import praw
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

def fetch_reddit_data():
    """Fetch top posts from Reddit."""
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    
    
    # 
    subreddit = reddit.subreddit('dataengineering')
    
    posts = []
    for post in subreddit.hot():
        print(post)
    print(subreddit.display_name)
 
# # display the subreddit title 
    print(subreddit.title)       
 
# # display the subreddit description 
    print(subreddit.description)
fetch_reddit_data()