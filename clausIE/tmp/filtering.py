# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import os
import string

# filtering the non-SVO out: we want SV and SVO now
def get_svo(PATH_SVO, PATH_SVO_NOACTORS):

    lemmatizer = WordNetLemmatizer()
    with open(PATH_SVO) as f:

        # preserve only SV or SVO or SVC
        results = []
        lines = f.readlines()
        for line in lines:
            line = [token.strip() for token in line.split(',') if token.strip()]
            initials = set([each[0] for each in line if each])
            if initials == set('SVO') or initials == set('SV') or initials == set('SVC'):
                results.append(line)
            # this step confirms that all 482 instances are included in either SVO, SV or SVC
        
        # 3 lists to store subject, verbs and objects (used for df construction)
        subject_lines = []
        verb_lines = []
        object_lines = []

        # convert SV, SVO, SVC all to SVO forms (write mid_svo)
        for line in results: # line: list of tuple pairs
            line_dict = {}
            for pair in line:
                pair = pair.split(':')
                if len(pair) == 2:
                    label = pair[0].strip()
                    word = pair[1].strip().strip('""').lower()
                    if label == 'V':
                        # word = stemmer.stem(word)
                        word = lemmatizer.lemmatize(word, 'v')
#                         print('%s: %s' % (label, word))
                    line_dict.update({label: word})
            
            # get S,V,O from dict
            subject_lines.append(line_dict['S'])
            verb_lines.append(line_dict['V'])
            if 'O' in line_dict:
                object_lines.append(line_dict['O'])
            elif 'C' in line_dict:
                object_lines.append(line_dict['C'])
            else:
                object_lines.append('')

        # convert into df structure
        final_svo = np.array([subject_lines, verb_lines, object_lines])
        final_svo = np.transpose(final_svo)
        df = pd.DataFrame(final_svo, columns=['Subject', 'Verb', 'Object'])
        print(df.head())
        print(len(df))
        df.to_csv(PATH_SVO_NOACTORS, index=False)


def filter_actors(NUM_SENT, PATH_ACTORS, PATH_SVO_NOACTORS, PATH_SVO_ACTORS):

    # read data and actors
    df = pd.read_csv(PATH_SVO_NOACTORS)
    actors = []
    with open(PATH_ACTORS) as f:
        for line in f.readlines():
            actors.extend(word_tokenize(line))
    actors = set(actor.lower() for actor in actors)

    df_actors = df.loc[df.Subject.isin(actors) | df.Object.isin(actors)]
    print(df_actors)
    df_actors.to_csv(PATH_SVO_ACTORS, index=False)

    

def svo_filter(number_sentences, actor_file_path, use_actors= False):
    PATH_ACTORS = os.path.join(actor_file_path, 'actors.txt')
    PATH_SVO = os.path.join(actor_file_path, 'raw_svo.txt')
    PATH_SVO_NOACTORS = os.path.join(actor_file_path, 'svo.csv')
    PATH_SVO_ACTORS = os.path.join(actor_file_path, 'svo_actors.csv')

    get_svo(PATH_SVO, PATH_SVO_NOACTORS)
    filter_actors(number_sentences, PATH_ACTORS, PATH_SVO_NOACTORS, PATH_SVO_ACTORS)

