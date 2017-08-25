# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import os
import string

# filtering the non-SVO out
def svo(PATH_SVO, PATH_SVO_MID):
    # stemmer = SnowballStemmer("english")
    lemmatizer = WordNetLemmatizer()
    with open(PATH_SVO) as f:
        results = []
        lines = f.readlines()
        for line in lines:
            line = [token.strip() for token in line.split(',') if token.strip()]
            initials = [each[0] for each in line if each]
            initials = set(''.join(initials))
            if initials == set('SVO'):
                results.append(line)
        with open(PATH_SVO_MID, 'w') as out:
    #       line: list of tuple pairs 
            for line in results:
                # print(line)
                line_dict = {}
                for i, pair in enumerate(line):
                    pair = pair.split(':')
                    if len(pair) == 2:
                        label = pair[0].strip()
                        word = pair[1].strip().strip('""').lower()
                        if label == 'V':
                            # word = stemmer.stem(word)
                            word = lemmatizer.lemmatize(word, 'v')
    #                         print('%s: %s' % (label, word))
                        line_dict.update({label: word})
                out.write('%s: %-15s, ' % ('S', line_dict['S']))
                out.write('%s: %-15s, ' % ('V', line_dict['V']))
                out.write('%s: %-15s' % ('O', line_dict['O']))
                out.write('\n')


def filter(NUM_SENT,PATH_ACTORS, PATH_SVO_MID, PATH_SVO_FINAL, PATH_CSV):
    # filtering SVO that is beyond our purpose
    # verbs
    # verb_df = pd.read_csv('verbs.csv')
    # print(verb_df.columns)
    # confirmed = verb_df['Confirmed social verb'].isnull()
    # idx = verb_df[confirmed==False].index.tolist()
    # verbs = set(verb_df.loc[idx]['Verb'].tolist())

    # actors
    # actors_df = pd.read_csv('actors.csv')
    # # print(actors_df.head())
    # confirmed = actors_df['Confirmed social noun'].isnull()
    # idx = actors_df[confirmed == False].index.tolist()
    # print(actors_df.loc[idx].head())
    # actors = actors_df.loc[idx]['Stanford Noun']
    final_svo = []
    if os.path.exists(PATH_ACTORS):
        actors = []
        with open(PATH_ACTORS) as f:
            for line in f.readlines():
                actors.extend(word_tokenize(line))
        actors = set(actor.lower() for actor in actors)
        with open(PATH_SVO_MID,'r') as f:
            lines = f.readlines()
            for l in lines:
                isConfirmed = True
                for pair in l.strip().split(','):
                    if len(pair.split(':'))==2:
                        label, word = pair.split(':')
                    else:
                        isConfirmed = False
                        break
                    label = label.strip()
                    word = word.strip()
                    # obtain the stem of word
                    if label == 'S' and word not in actors:
                        isConfirmed = False
                        break
                    if label == 'S' and word in ['her', 'his', 'its', 'their','my','our']:
                        isConfirmed = False
                        break
                if isConfirmed:
                    final_svo.append(l)
            with open(PATH_SVO_FINAL, 'w') as out:
                print('There are %d number of SVOs extracted from %d input sentences.' % (len(final_svo), NUM_SENT))
                for line in final_svo:
                    out.write(line)
    #             out.write('\n')
    if not os.path.exists(PATH_ACTORS):
        with open(PATH_SVO_MID,'r') as f:
            lines = f.readlines()
            for l in lines:
                isConfirmed = True
                for pair in l.strip().split(','):
                    if len(pair.split(':'))==2:
                        label, word = pair.split(':')
                    else:
                        isConfirmed = False
                        break
                    label = label.strip()
                    word = word.strip()
                    if label == 'S' and word in string.punctuation:
                        isConfirmed = False
                        break
                    if label == 'S' and word in ['her', 'his', 'its', 'their','my','our']:
                        isConfirmed = False
                        break
                if isConfirmed:
                    final_svo.append(l)
        with open(PATH_SVO_FINAL, 'w') as out:
            print('There are %d number of SVOs extracted from %d input sentences.' % (len(final_svo), NUM_SENT))
            for line in final_svo:
                out.write(line)
    # print(final_svo)
    lines = []
    for line in final_svo:
        line = line.split(',')
        line = [pair.split(':')[1].strip() for pair in line]
        # print(line)
        lines.append(line)
    df = pd.DataFrame(lines, columns=['Node1', 'Edge', 'Node2'])
    print(df.head())
    df.to_csv(PATH_CSV)

def svo_filter(NUM_SENT, PATH_OUT):
    PATH_ACTORS = '/'.join([PATH_OUT, 'actors.txt'])
    PATH_SVO = '/'.join([PATH_OUT, 'svo.txt'])
    PATH_SVO_MID = '/'.join([PATH_OUT, 'mid_svo.txt'])
    PATH_SVO_FINAL = '/'.join([PATH_OUT, 'final_svo.txt'])
    PATH_CSV = '/'.join([PATH_OUT, 'SVO.CSV'])

    svo(PATH_SVO, PATH_SVO_MID)
    filter(NUM_SENT, PATH_ACTORS, PATH_SVO_MID, PATH_SVO_FINAL, PATH_CSV)

