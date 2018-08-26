import pandas as pd
import numpy as np
import dill
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Twitter


western_data = pd.read_csv('static/western_preprocessed.csv')
test2_img = pd.read_excel('static/data/test2_img_drop2.xlsx')
art2vec = Word2Vec.load('static/data/word2vec_test2_img_tw.w2v')


with open('static/data/test2_img_drop_word_vector.dill', 'rb') as fp:
    test2_word_vector = dill.load(fp)
with open('static/data/western_noun_adj.dill', 'rb') as fp:
    western_noun_adj = dill.load(fp)


twitter = Twitter()


def Cos_Sim(test_txt_list):

    word_vector1 = np.zeros(100, dtype='float32')

    for word in test_txt_list:
        lenth = len(test_txt_list)
        try:
            word_vector1 += art2vec.wv.get_vector(word)
        except:
            lenth -= 1

    if lenth != 0:
        word_vector1 = word_vector1 / lenth
    else:
        word_vector1 = np.zeros(100, dtype='float32')

    result = art2vec.wv.cosine_similarities(word_vector1,
                                            [test2_word_vector[i][1] for i in range(len(test2_word_vector))])

    result_sorted = np.sort(result)
    result_index = np.argsort(result)
    result_sorted = result_sorted[::-1]
    result_index = result_index[::-1]

    result_drop_nan = []

    for i in range(len(result_sorted)):
        if np.isnan(result_sorted[i]):
            pass
        else:
            result_drop_nan.append((result_index[i], result_sorted[i]))

    return result_drop_nan


