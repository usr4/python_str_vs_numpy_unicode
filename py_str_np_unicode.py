import sys
import time

from nltk.corpus import brown
import numpy as np

def py_str_vs_np_str_rank_0(words, str_):

    print('Python str: {:>10} bytes'.format(sys.getsizeof(str_)))

    np_str = np.array(str_, dtype=np.unicode_)
    print('Numpy str:  {:>10} bytes'.format(sys.getsizeof(np_str)))
    
    start = time.time()
    for w in words[:1000]:
        _ = str_.find(w)
    print('Python find: {:>10.5f} sec'.format(time.time() - start))
    
    start = time.time()
    for w in words[:1000]:
        _ = np.char.find(np_str, w)
    print('Numpy find:  {:>10.5f} sec'.format(time.time() - start))

def py_str_vs_np_str_rank_1(words):

    print('Python str: {:>10} bytes'.format(sys.getsizeof(words)))
    
    np_words = np.array(words, dtype=np.unicode_)
    print('Numpy str:  {:>10} bytes, dtype={}'.format(
        sys.getsizeof(np_words), np_words.dtype))

def py_str_vs_np_str_rank_2(words, shape1):

    shape0 = len(words) // shape1
    print('shape=({}, {})'.format(shape0, shape1))
    
    rank2_words = list()
    for i in range(0, shape0):
        rank2_words.append(words[i:i+shape1])
    print('Python str: {:>10} bytes'.format(
        sys.getsizeof(rank2_words) + \
        sum([sys.getsizeof(e) for e in rank2_words])))
    
    np_words = np.array(rank2_words, dtype=np.unicode_)
    print('Numpy str:  {:>10} bytes, dtype={}'.format(
        sys.getsizeof(np_words), np_words.dtype))
    
if __name__ == '__main__':

    words = list(brown.words())
    str_ = ''.join(words)
    print(len(words), 'words,', len(str_), 'chars')
    
    d = dict()
    for w in words:
        if len(w) in d:
            d[len(w)].append(w)
        else:
            d[len(w)] = [w]
    
    for k in sorted(d.keys()):
        print('Number of {:>2}-letter words: {:>6}'.format(k, len(d[k])))
    
    print('Rank0')
    py_str_vs_np_str_rank_0(words, str_)

    print('Rank1')
    py_str_vs_np_str_rank_1(words)

    for i in range(1, 4):
        print('Rank1({}-letter words)'.format(i))
        py_str_vs_np_str_rank_1(d[i])

    print('Rank2')
    py_str_vs_np_str_rank_2(words, 100)

    for i in range(1, 4):
        print('Rank2({}-letter words)'.format(i))
        py_str_vs_np_str_rank_2(d[i], 100)

    print('Rank2')
    py_str_vs_np_str_rank_2(words, 10)

    for i in range(1, 4):
        print('Rank2({}-letter words)'.format(i))
        py_str_vs_np_str_rank_2(d[i], 10)
