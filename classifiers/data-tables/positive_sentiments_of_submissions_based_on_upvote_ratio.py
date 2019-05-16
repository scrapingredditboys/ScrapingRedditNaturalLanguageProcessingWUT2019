import pandas as pd
import numpy as np

#Only few data was available in the comments database for this.
df = pd.read_csv('sample.csv')
df.head()

m = []
upvote_r = []
x = 0

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('sentiment_karma_submissions_{0}.csv'.format(subreddit_id))
  
  #sorting data frame by Team and then By names 
  submission.sort_values(["upvote_ratio"], axis=0, 
                 ascending=True, inplace=True)
  
  
  sub_new = submission.groupby(['upvote_ratio'], as_index=False)['sentiment_pos_title'].mean()
    
  for row in sub_new['upvote_ratio']:
      upvote_r.insert(x, row)
      x+=1
	  
	 
	 
upvote_r = sorted(set(upvote_r))
df['upvote_ratio'] = upvote_r

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('sentiment_karma_submissions_{0}.csv'.format(subreddit_id))
   
  df.insert(i + 1, subreddit_name, 0, True)
  
  
for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('sentiment_karma_submissions_{0}.csv'.format(subreddit_id))
  
  #sorting data frame by Team and then By names 
  submission.sort_values(["upvote_ratio"], axis=0, 
                 ascending=True, inplace=True)
  
  sub_new = submission.groupby(['upvote_ratio'], as_index=False)['sentiment_pos_title'].mean()
  
  karma_by_comments_length = []
  x = 0
  for j in upvote_r:
      karma = sub_new.loc[sub_new['upvote_ratio'] == j , 'sentiment_pos_title']
      meany = karma.mean()
      df.iloc[x, df.columns.get_loc(subreddit_name)] = "{0:.3f}".format(meany)
      x+=1
	  
df.to_csv('negative_sentiments_of_submissions_based_on_upvote_ratio.csv', index=None, header=True)