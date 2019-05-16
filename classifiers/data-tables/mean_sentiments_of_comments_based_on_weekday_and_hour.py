import pandas as pd
import numpy as np

df = pd.read_csv('sample.csv')
df.head()


for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('sentiment_comment_timing_{0}.csv'.format(subreddit_id))

  
  sentiment_on_day_hour_mean = []
  x = 0
  for days in range(7):
    for hours in range(24): 
        interval = submission[(submission['weekday'] == days ) & (submission['hour'] == hours)]
        sentiment_pos = interval.loc[interval['hour'] == hours, 'sentiment_pos']
        sentiment_neg = interval.loc[interval['hour'] == hours, 'sentiment_neg']
        meany = (sentiment_pos - sentiment_neg).astype(float)
        sentiment_on_day_hour_mean.insert(x,  list(map('{:.3f}'.format,meany)))
        x += 1
        
  df.insert(i + 2, subreddit_name,sentiment_on_day_hour_mean, True)
  df[subreddit_name] = df[subreddit_name].str.get(0)
  
  
df  
df.to_csv('mean_sentiments_of_comments_based_on_weekday_and_hour.csv', index=None, header=True)