import pandas as pd
from sqlalchemy import create_engine
from multiprocessing.dummy import Pool as ThreadPool
import re

from sqlalchemy.util import NoneType

import os.path

engine = create_engine('postgresql://postgres@localhost:5432/reddit')


def subreddit_resolve(name):
    if os.path.isfile("submission_count_{0}.csv".format(name)):
        return
    submissions = pd.read_sql_query(
        "SELECT * FROM submissions where subreddit_id=\'{0}\'".format(name),
        con=engine)
    df = pd.DataFrame(columns=["word", "uses", "unique", "score"])
    df.set_index('word', drop=True, inplace=True)

    df2 = pd.DataFrame(columns=["word", "uses", "unique", "score"])
    df2.set_index('word', drop=True, inplace=True)

    count = submissions['id'].count()
    for submission_index, submission_row in submissions.iterrows():
        print("Submission: {0}/{1}".format(submission_index + 1, count))
        if type(submission_row['title']) is not NoneType:
            words = submission_row['title'].lower().split(" ")
        else:
            words = []
        if type(submission_row['selftext']) is not NoneType:
            words.extend(submission_row['selftext'].lower().split(" "))

        for word in set(words):
            if word not in df.index:
                df.loc[word] = [0] * df.columns.size
            df["unique"][word] += 1
            df["score"][word] += submission_row['score']
        for word in words:
            df['uses'][word] += 1

        # Comments
        comments = pd.read_sql_query(
            "SELECT * FROM comments where submission_id=\'" + submission_row['id'] + "\'",
            con=engine)

        for _, comment_row in comments.iterrows():
            if type(comment_row['body']) is NoneType:
                continue
            comment_words = comment_row['body'].lower().split(" ")
            for word in comment_words:
                if word not in df2.index:
                    df2.loc[word] = [0] * df2.columns.size
                df2['uses'][word] += 1
            for word in set(comment_words):
                df2["unique"][word] += 1
                df2["score"][word] += comment_row['score']

    df.sort_values(["score"], ascending=False, inplace=True)
    df2.sort_values(["score"], ascending=False, inplace=True)
    df.to_csv(path_or_buf="submission_count_{0}.csv".format(name))
    df2.to_csv(path_or_buf="comment_count_{0}.csv".format(name))


subreddits = pd.read_sql_table("subreddits", con=engine)
subreddits = subreddits.sample(frac=1)
selection = input("Subreddit name:")
if selection == "":
    pool = ThreadPool(4)
    pool.map(subreddit_resolve, subreddits['id'])
else:
    results = subreddits.where(subreddits['display_name'] == selection).dropna()
    subreddit_resolve(results.iloc[0]['id'])
