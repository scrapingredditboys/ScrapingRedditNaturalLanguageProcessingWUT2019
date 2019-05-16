import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
%matplotlib inline 

df = pd.read_csv('sample.csv')
df.head()


m = []

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('karma_comments_{0}.csv'.format(subreddit_id))
  
  #sorting data frame by Team and then By names 
  submission.sort_values(["length"], axis=0, 
                 ascending=True, inplace=True)
  
  sub_new = submission.groupby(['length'], as_index=False)['score'].mean()
  
  len_sub_new = sub_new['length']
  karma_by_comments_length = []
  m.append(len_sub_new.count())  
  
m

maxxy = max(m)
numm = []
for i in range(0, maxxy):
     numm.insert(i, i+1)

df['comment_length'] = numm
df

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('karma_comments_{0}.csv'.format(subreddit_id))
   
  df.insert(i + 1, subreddit_name, 0, True) 
  
df


for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  
  submission = pd.read_csv('karma_comments_{0}.csv'.format(subreddit_id))
  
  #sorting data frame by Team and then By names 
  submission.sort_values(["length"], axis=0, 
                 ascending=True, inplace=True)
  
  sub_new = submission.groupby(['length'], as_index=False)['score'].mean()
  
  len_sub_new = sub_new['length']
  print(len_sub_new.count())
  karma_by_comments_length = []
  x = 0
  for j in len_sub_new:
      karma = sub_new.loc[sub_new['length'] == j , 'score']
      meany = karma.mean()
      df.iloc[x, df.columns.get_loc(subreddit_name)] = "{0:.3f}".format(meany)
      x+=1     
   

df.to_csv('karma_of_comments_based_on_comment_length.csv', index=None, header=True)   
  
