
# coding: utf-8

# In[60]:


import glob
import os
import re
from nltk.tokenize import sent_tokenize
import string
import sys
import enchant
Title_length_limit = 50
# FOR AJS
# doc_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/AJS'
# titles_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/AJS_titles'
# data_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/AJS_Processed'
# FOR ASR
doc_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/ASR'
titles_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/ASR_titles'
data_path = '/Users/apple/Desktop/Roberto-Research/PROCESSED_AJS_ASR/ASR_Processed'


# In[61]:

def isSentence(sentence):
    if len(sentence.split()) < 5:
        return False
#     if sentence.split()[0].isnumeric():
#         return False
    if sentence[-1] not in string.punctuation:
        return False
    if sentence.isupper():
        return False
    if sentence.istitle():
        return False
    count = 0
    for token in sentence.split():
        if len(token) >=2 and token.isupper():
            count += 1
        if token.strip('.').isnumeric():
            count += 1
        elif token in ['p.', 'Vol.', 'pp.', 'Published']:
            count +=3
        if count >=3:
            return False
    return True


# In[62]:

def isTitle(sentence):
	if sentence[-1] not in string.punctuation:
		if len(sentence) < Title_length_limit:
			# print sentence
			return True
	if sentence.isupper():
		# print sentence
		return True
	if sentence.istitle():
		# print sentence
		return True


# In[63]:

# handle broken words
def merge_words(sentences):
    dictionary = enchant.Dict("en_US")
    merged_sentences = []

    for sent in sentences:
        sent = sent.split()
        i = 0
        newsent = []
        while i < len(sent)-1:
            if (not dictionary.check(sent[i]) or not dictionary.check(sent[i+1])) and (dictionary.check(sent[i]+sent[i+1].lower()) or dictionary.check(sent[i]+sent[i+1].lower()[:-1])):
                newword = sent[i]+sent[i+1].lower()
                newsent.append(newword)
                i += 2
            else:
                newsent.append(sent[i])
                i += 1
        lastword = sent[len(sent)-1]
        if dictionary.check(lastword):
            newsent.append(lastword)
        merged_sentences.append(' '.join(newsent))
    return merged_sentences


# In[64]:

# titles 
# abstracts, contents
def process():
    for file in glob.glob(os.path.join(data_path, '*.txt')):
        filename = file.split('/')[-1]
        sentences = []
        Badsentences = []
        with open(file, 'r') as f:
            lines = f.read()
            lines = sent_tokenize(lines.decode('utf-8'))
            print('The original number of lines is %d' % len(lines))
            for line in lines:
                tokens = []
                for token in line.split():
                    if token.strip():
                        tokens.append(token)
                line = ' '.join(tokens)
                if isSentence(line):
                    sentences.append(line)
                else:
                    Badsentences.append(line)
            print("The new number of lines is %d \n" % len(sentences))
        with open(os.path.join(titles_path, filename), 'w') as titleout:
            for bad in Badsentences:
#               if isTitle(bad):
                titleout.write(bad.encode('utf-8'))
                titleout.write('\n')

        with open(os.path.join(doc_path, filename), 'w') as out:
            sentences = merge_words(sentences)
            for sent in sentences:
                # print sent, '\n'
                out.write(sent.encode('utf-8'))
                out.write(' ')


# In[65]:

if __name__=="__main__":
	process()


# In[84]:

# for file in glob.glob(os.path.join(data_path, '*.txt')):
#     filename = file.split('/')[-1]
#     with open(file, 'r') as f:
#         lines = f.read().strip()
#         lines = sent_tokenize(lines)
#         for line in lines:
#             print(line)
#             print('\n')
#         break


# In[24]:

# lines = '''385-397 Published by: The University of Chicago Press Stable URL: http://www.jstor.org/stable/2761870 Accessed: 08-05-2016 22:26 UTC Competitive commercial life is not a flowery bed of ease, but a battle field where the "struggle for existence " is defining the industrially "fittest to survive."
# '''
# for line in lines.split():
#     print(line)


# In[ ]:



