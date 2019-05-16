import pandas as pd
import numpy as np

#empty sample csv containing weekday and hour columns only
df = pd.read_csv('sample.csv')
df.head()

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('comment_timing_{0}.csv'.format(subreddit_id))

  
  comments_on_day_hour = []
  x = 0
  for days in range(7):
    for hours in range(24): 
        interval = submission[(submission['weekday'] == days ) & (submission['hour'] == hours)]
        comments = interval.loc[interval['hour'] == hours, 'comments']
        comments_on_day_hour.insert(x,  int(comments))
        x += 1
        
  df.insert(i + 2, subreddit_name,comments_on_day_hour, True)
   
  
df.to_csv('number_of_comments_based_on_weekday_and_hour.csv', index=None, header=True)