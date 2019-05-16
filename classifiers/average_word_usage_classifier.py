import numpy as np
import pandas as pd
import collections
from collections import defaultdict

def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters.""" 
    for ord_ in range(ord(start.lower()), ord(stop.lower()), step):
        yield chr(ord_)
		
list_of_word = []
list_of_sub = []
list_of_ratio = []
for i in list(letter_range("a", "d")):
    avg = pd.read_csv('average_usage_of_words_trial{0}.csv'.format(i))
    
    for word in avg['Words']:
        list_of_word.append(word)
        
    for sub in avg['Subreddits']:
        list_of_sub.append(sub)
        
    for ratio in avg['Ratio']:
        list_of_ratio.append("{0:.3f}".format(ratio))
	
print(len(list_of_word), len(list_of_sub), len(list_of_ratio))
res = [(i, j, k) for i, j, k in zip(list_of_word, list_of_sub, list_of_ratio)]
print(len(res))
res

without = []
for i in res:
        if i[2] > "{0:.3f}".format(0.05):
                without.append(i)

print(len(without))

wordy = []
for i in without:
    wordy.append(i[0])
	
wordy = list(dict.fromkeys(wordy))
print(len(wordy))
wordy				
	
df = pd.DataFrame(wordy , columns = ['Words'])

for i in range(55):
  subreddit =  pd.read_csv('subreddits.csv')
  subreddit_id = subreddit.iloc[i]['id']   #change here for new id
  subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name

  df.insert(i + 1, subreddit_name, "{0:.3f}".format(0), True) 
  
  
count = 0
for i in range(55):
    subreddit =  pd.read_csv('subreddits.csv')
    subreddit_id = subreddit.iloc[i]['id']   #change here for new id
    subreddit_name = subreddit.iloc[i]['display_name'] #change here for new name
    result = {}
   
    for word,subred,uses in res:
        if subred == subreddit_name and word in wordss: #change for each
            result[word] = uses	
            
     
    print(count,"Length",len(result))
    count += 1
    for idx, j in enumerate(df['Words']):
        for k, v in result.items():
              if  k == j:
                  df.at[idx, subreddit_name] = v
                  continue
				  
df
df.to_csv('average_word_usage_classifier.csv', index=None, header=True)