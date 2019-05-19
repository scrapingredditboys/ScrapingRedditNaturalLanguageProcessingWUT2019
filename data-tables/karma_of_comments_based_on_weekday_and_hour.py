import pandas as pd
import numpy as np
import os

#Contains predefined Weekday and hour columns
df = pd.read_csv('sample.csv')
df.head()

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('submission_timing_{0}.csv'.format(subreddit_id))

  
  karma_on_day_hour= []
  submission_on_day_hour = []
  
  x = 0
  for days in range(7):
    for hours in range(24): 
        interval = submission[(submission['weekday'] == days ) & (submission['hour'] == hours)]
        karma = interval.loc[interval['hour'] == hours, 'karma']
        no_of_submission = interval.loc[interval['hour'] == hours , 'submissions']
        karma_on_day_hour.insert(x,  "{0:.f}".format(karma.mean()))
		submission_on_day_hour.insert(x,  "{0:.f}".format(no_of_submission.meany()))
        x += 1
        


#df to csv
df.to_csv('karma_of_comments_based_on_weekday_and_hour.csv', index=None, header=True)