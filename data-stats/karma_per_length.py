import pandas as pd
import pandas.io as io
from sqlalchemy import create_engine
import threading
from multiprocessing.dummy import Pool as ThreadPool 
import re
engine = create_engine('postgresql://postgres:password123@localhost:5432/reddit')


def subreddit_length(name):
    df = pd.DataFrame(columns=["title_length", "selftext_length", "score"])
    df2 = pd.DataFrame(columns=["length", "score"])

    submissions = pd.read_sql_query(
            "SELECT * FROM submissions where subreddit_id=\'{0}\'".format(name),
            con=engine)
    for submission_index,submission_row in submissions.iterrows():
        print("Submission: {0}/{1}".format(submission_index+1, submissions['id'].count()))
        title_length = len(submission_row['title'])
        selftext_length = len(submission_row['selftext'])
        df.loc[len(df)] = [title_length, selftext_length, submission_row['score']]

        # Comments
        comments = pd.read_sql_query(
            "SELECT * FROM comments where parent_id=\'"+submission_row['id']+"\'",
            con=engine)
        for _,comment_row in comments.iterrows():
            comment_length = len(comment_row['body'])
            df2.loc[len(df2)] = [comment_length, comment_row["score"]]

    df.sort_values(["score"], ascending=False)
    df2.sort_values(["score"], ascending=False)
    df.to_csv(path_or_buf="karma_submissions_{0}.csv".format(name))
    df2.to_csv(path_or_buf="karma_comments_{0}.csv".format(name))


subreddits = pd.read_sql_table("subreddits", con=engine)
selection = input("Subreddit name:")
if selection == "all":
    pool = ThreadPool(4) 
    pool.map(subreddit_length, subreddits['id'])
else:
    results = subreddits.where(subreddits['display_name']==selection).dropna()
    subreddit_length(results.iloc[0]['id'])