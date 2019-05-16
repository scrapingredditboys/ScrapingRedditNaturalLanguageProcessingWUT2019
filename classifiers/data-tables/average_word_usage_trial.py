import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import collections
from itertools import groupby 
%matplotlib inline 
from collections import defaultdict


list_of_subreddit = []
list_of_word = []
list_of_uses = []
for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
  submission = pd.read_csv('comment_count_{0}.csv'.format(subreddit_id))  
      
  for word in submission['word']:
      list_of_word.append(word)
      list_of_subreddit.append(subreddit_name)

  for uses in submission['uses']:
         list_of_uses.append(uses)
		 
		 
		 
res = [(i, j, k) for i, j, k in zip(list_of_word, list_of_subreddit, list_of_uses)]
print(len(res))
res


result = {}
for word,subred,uses in res:
        total = result.get(word,0) + uses
        result[word] = total
		
		
print(len(result))
result = [(i, j) for i, j in result.items() if j > 26]
print(len(result))
result = [(i) for i in result if i[0] not in stopwords.words('english')]
print(len(result))


end = []
counter = 0
for i in result: 
    for j in res:
        if i[0] == j[0]:
            print(counter)
            end.append((j[0], j[1], j[2], i[1], "{0:.3f}".format(j[2]/i[1]) ))
            counter +=1
			
end

df = pd.DataFrame(end, columns = ['Words', 'Subreddits', 'Usage', 'Total Usage', 'Ratio'])

df.to_csv('average_usage_of_words_trial.csv', index=None, header=True)  #For a, b, c and d