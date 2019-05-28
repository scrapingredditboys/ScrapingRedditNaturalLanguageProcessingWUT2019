# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KPFjaZbLsaRjjHPCWj8MtOkYpcSAei49
"""

import numpy as np
import pandas as pd
import collections
from collections import defaultdict

lexicon = pd.read_csv('lexicon.csv', sep = ';')
lexicon

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

unique_words = []
for i in lexicon['Word']:
    unique_words.append(i)
unique_words

without = []
for i in res:
    if i[2] > "{0:.3f}".format(0.076):  
      if i[0] in unique_words:
          without.append(i)
                
print(len(without))

wordy = []
for i in without:
    wordy.append(i[0])
    
wordy = list(dict.fromkeys(wordy))
print(len(wordy))
wordy

df = pd.DataFrame(columns=lexicon.columns)

for number in range(len(lexicon)):
    if lexicon.loc[number, 'Word'] in wordy:
      df = df.append(lexicon.loc[number])

df
df.to_csv('TopicsClassifier.csv', index=None, header=True)