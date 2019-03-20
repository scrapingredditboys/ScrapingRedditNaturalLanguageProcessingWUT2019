import pandas as pd
import pandas.io as io
from sqlalchemy import create_engine
import threading
from multiprocessing.dummy import Pool as ThreadPool 
import re
engine = create_engine('postgresql://postgres:password123@localhost:5432/reddit')


def subreddit_time(name):
    df = pd.DataFrame(columns=["weekday", "hour", "submissions", "karma"])
    df2 = pd.DataFrame(columns=["weekday", "hour", "comments", "comments_length", "karma"])
    df["hour"] = list(range(0, 24))*7
    df2["hour"] = list(range(0, 24))*7
    for i in range(0, 7):
        df["weekday"][i*24:(i+1)*24] = [i]*24
        df2["weekday"][i*24:(i+1)*24] = [i]*24
    df.fillna(value=0, inplace=True)
    df2.fillna(value=0, inplace=True)
    df.set_index(['weekday', 'hour'], inplace=True, drop=True)
    df2.set_index(['weekday', 'hour'], inplace=True, drop=True)

    submissions = pd.read_sql_query(
            "SELECT * FROM submissions where subreddit_id=\'{0}\'".format(name),
            con=engine, parse_dates=["created_utc"])
    for submission_index, submission_row in submissions.iterrows():
        print("Submission: {0}/{1}".format(submission_index+1, submissions['id'].count()))
        hour = submission_row['created_utc'].hour
        weekday = submission_row['created_utc'].weekday()
        karma = submission_row['score']
        df['submissions'][weekday, hour] += 1
        df['karma'][weekday, hour] += karma
        comments = pd.read_sql_query(
            "SELECT * FROM comments where parent_id=\'"+submission_row['id']+"\'",
            con=engine, parse_dates=["created_utc"])
        for _, comment_row in comments.iterrows():
            hour = comment_row['created_utc'].hour
            weekday = comment_row['created_utc'].weekday()
            length = len(comment_row['body'])
            karma = comment_row['score']
            df2['comments'][weekday, hour] += 1
            df2['comments_length'][weekday, hour] += length
            df2['karma'][weekday, hour] += karma

    df.to_csv(path_or_buf="submission_timing_{0}.csv".format(name))
    df2.to_csv(path_or_buf="comment_timing_{0}.csv".format(name))

subreddits = pd.read_sql_table("subreddits", con=engine)
selection = input("Subreddit name:")
if selection == "all":
    pool = ThreadPool(4) 
    pool.map(subreddit_time, subreddits['id'])
else:
    results = subreddits.where(subreddits['display_name']==selection).dropna()
    subreddit_time(results.iloc[0]['id'])