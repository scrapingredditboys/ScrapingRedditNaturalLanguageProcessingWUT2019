import pandas as pd
import numpy as np
import os

#reading a predefined empty csv
df = pd.read_csv('karma_by_hour_of_posting.csv')
df.head()

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('comment_timing_{0}.csv'.format(subreddit_id))

  karma_on_hour_mean = []
  for j in range(24):
    comments = submission.loc[submission['hour'] == j, 'comments']
    karma = submission.loc[submission['hour'] == j, 'karma']
    meany = (karma/comments).mean()
    karma_on_hour_mean.insert(j,  "{0:.3f}".format(meany))

  df.insert(i + 1, subreddit_name,karma_on_hour_mean, True) 
  
  
#df to csv
 df.to_csv('karma_of_comments_based_on_hour.csv', index=None, header=True)