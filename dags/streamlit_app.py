import streamlit as st
import pandas as pd
import os

# Path to the CSV file
CSV_PATH = "/tmp/reddit_data.csv"  # Ensure this matches the path in Airflow

# Load the data
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        st.error("❌ Data file not found!")
        return None

def main():
    st.title("📊 Reddit Data Dashboard")
    st.sidebar.header("Filters")
    
    df = load_data()
    if df is None:
        return
    
    # Convert UTC timestamp to datetime if it exists
    if 'created_utc' in df.columns:
        df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    
    # Filters
    subreddit_list = df['subreddit'].unique() if 'subreddit' in df.columns else []
    selected_subreddit = st.sidebar.selectbox("Select Subreddit", ['All'] + list(subreddit_list))
    
    if selected_subreddit != 'All':
        df = df[df['subreddit'] == selected_subreddit]
    
    # Metrics
    st.metric("Total Posts", len(df))
    if 'score' in df.columns:
        st.metric("Average Score", round(df['score'].mean(), 2))
    if 'num_comments' in df.columns:
        st.metric("Average Comments", round(df['num_comments'].mean(), 2))
    
    # Show data
    st.subheader("Top Posts")
    st.dataframe(df[['title', 'score', 'num_comments', 'created_utc']].sort_values(by='score', ascending=False).head(10))
    
    # Visualization
    if 'score' in df.columns and 'created_utc' in df.columns:
        st.subheader("Score Over Time")
        st.line_chart(df.set_index('created_utc')['score'])

if __name__ == "__main__":
    main()