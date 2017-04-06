# coding: utf-8

import pandas as pd
import numpy as np
import nltk
from nltk.stem.snowball import SnowballStemmer

# filtering the non-SVO out
def svo():
    stemmer = SnowballStemmer("english")
    with open('svo.txt') as f:
        results = []
        lines = f.readlines()
        for line in lines:
            line = [token.strip() for token in line.split(',') if token.strip()]
            initials = [each[0] for each in line if each]
            initials = set(''.join(initials))
            if initials == set('SVO'):
                results.append(line)
        with open('final_svo.txt', 'w') as out:
    #       line: list of tuple pairs 
            for line in results:
                line_dict = {}
                for i, pair in enumerate(line):
                    pair = pair.split(':')
                    if len(pair) == 2:
                        label = pair[0].strip()
                        word = pair[1].strip().strip('""').lower()
                        if label == 'V':
                            word = stemmer.stem(word)
    #                         print('%s: %s' % (label, word))
                        line_dict.update({label: word})
                out.write('%s: %-15s, ' % ('S', line_dict['S']))
                out.write('%s: %-15s, ' % ('V', line_dict['V']))
                out.write('%s: %-15s' % ('O', line_dict['O']))
                out.write('\n')


def filter(NUM_SENT):
    # filtering SVO that is beyond our purpose
    # verbs
    verb_df = pd.read_csv('verbs.csv')
    # print(verb_df.columns)
    confirmed = verb_df['Confirmed social verb'].isnull()
    idx = verb_df[confirmed==False].index.tolist()
    verbs = set(verb_df.loc[idx]['Verb'].tolist())

    # actors
    actors_df = pd.read_csv('actors.csv')
    # print(actors_df.head())
    confirmed = actors_df['Confirmed social noun'].isnull()
    idx = actors_df[confirmed == False].index.tolist()
    # print(actors_df.loc[idx].head())
    actors = actors_df.loc[idx]['Stanford Noun']
    actors = set(actor.lower() for actor in actors)
    with open('final_svo.txt','r') as f:
        final_svo = []
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
                # if label =='V' and word not in verbs:
                #     isConfirmed = False
                #     break
            if isConfirmed:
                final_svo.append(l)
        with open('terminal_svo.txt', 'w') as out:
            print('There are %d number of SVOs extracted from %d input sentences.' % (len(final_svo), NUM_SENT))
            for line in final_svo:
                out.write(line)
    #             out.write('\n')


def svo_filter(NUM_SENT):
    svo()
    filter(NUM_SENT)

