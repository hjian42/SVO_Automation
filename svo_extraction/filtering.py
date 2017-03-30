
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[21]:

# filtering the non-SVO out
import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
with open('svo.txt') as f:
    results = []
    lines = f.readlines()
    for line in lines:
        line = [token.strip() for token in line.split(',')]
        initials = [each[0] for each in line if each]
        initials = set(''.join(initials))
        if initials == set('SVO'):
            results.append(line)
    with open('final_svo.txt', 'w') as out:
        for line in results:
#             print(line)
            for i, pair in enumerate(line):
#                 print(pair)
                pair = pair.split(':')
                if len(pair) == 2:
                    label = pair[0].strip()
                    word = pair[1].strip().strip('""').lower()
                    word = stemmer.stem(word)
                    print('%s: %s' % (label, word))
                    if i < 2:
                        out.write('%s: %s, ' % (label, word))
                    else:
                        out.write('%s: %s' % (label, word))
                else:
                    break
            out.write('\n')


# In[14]:

# filtering SVO that is beyond our purpose
verb_df = pd.read_csv('verbs.csv')
print(verb_df.columns)
verb_df.head()


# In[15]:

confirmed = verb_df['Confirmed social verb'].isnull()


# In[16]:

idx = verb_df[confirmed==False].index.tolist()


# In[17]:

verbs = set(verb_df.loc[idx]['Verb'].tolist())


# In[18]:

actors_df = pd.read_csv('actors.csv')
# print(actors_df.head())
confirmed = actors_df['Confirmed social noun'].isnull()
idx = actors_df[confirmed == False].index.tolist()
# print(actors_df.loc[idx].head())
actors = set(actors_df.loc[idx]['Stanford Noun'])


# In[24]:


with open('final_svo.txt','r') as f:
    final_svo = []
    lines = f.readlines()
    for l in lines:
        isConfirmed = True
        for pair in l.strip().split(','):
#             print(pair)
            if len(pair.split(':'))==2:
                label, word = pair.split(':')
            else:
                isConfirmed = False
                break
            label = label.strip()
            word = word.strip()
#           obtain the stem of word
            if label == 'S' and word not in actors:
                isConfirmed = False
                break
            if label =='V' and word not in verbs:
                isConfirmed = False
                break
        if isConfirmed:
            final_svo.append(l)
#         print(final_svo)
    with open('terminal_svo.txt', 'w') as out:
        print('There are %d number of SVOs extracted from 100 lynching articles.' % len(final_svo))
        for line in final_svo:
            out.write(line)
#             out.write('\n')


# In[ ]:



