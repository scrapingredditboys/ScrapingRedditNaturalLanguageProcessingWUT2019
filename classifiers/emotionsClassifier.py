import numpy as np
import pandas as pd
import collections
from collections import defaultdict

readingEmotions = pd.read_csv('emotions.csv')
readingEmotions

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

words_in_emo = []
for i in readingEmotions['Word']:
    words_in_emo.append(i)
words_in_emo

without = []
for i in res:
    if i[2] > "{0:.3f}".format(0.076):  
      if i[0] in words_in_emo:
          without.append(i)
                
print(len(without))

wordy = []
for i in without:
    wordy.append(i[0])
    
wordy = list(dict.fromkeys(wordy))
print(len(wordy))
wordy

df = pd.DataFrame(wordy, columns = ['Words'])
df.insert(1, "Valence", 0.0)
df.insert(2, "Arousal", 0.0)
df.insert(3, "Dominance", 0.0)
length = df['Words']
length
for idx, i in enumerate(df['Words']):
  abc = readingEmotions.loc[i]
  df.at[idx, 'Valence'] = "{0:.3f}".format(abc.Valence)
  df.at[idx, 'Arousal'] = "{0:.3f}".format(abc.Arousal)
  df.at[idx, 'Dominance'] = "{0:.3f}".format(abc.Dominance)
df

df
df.to_csv('EmotionsClassifier.csv', index=None, header=True)