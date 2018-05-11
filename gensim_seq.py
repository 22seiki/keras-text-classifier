from gensim import corpora, matutils, models
import os
import glob
import json
import sys
from scipy import sparse
import numpy as np

root_dir = "./text"
dic_file = root_dir + "/word-dic_gensim_svm.json"
data_file = root_dir + "/data_gensim_svm.json"

wakati_ID = []

# 単語にIDを振る
for cat in os.listdir(root_dir):
    cat_dir = root_dir + "/" + cat
    if not os.path.isdir(cat_dir):
        continue
    files = glob.glob(cat_dir + "/*.wakati")
    for path in files:
        print(path)
        if path.find(".wakati") == -1:
            continue
        with open(path, "r") as f:
            text = f.read().strip()
            words = text.split(" ")
            wakati_ID.append(words)

gensim_dic = corpora.Dictionary(wakati_ID)
# print(dictionary.token2id)

print("単語数=", len(gensim_dic))  # 次元の大きさ

gensim_dic.filter_extremes(no_below=30, no_above=0.3)
# no_berow: 使われてる文章がno_berow個以下の単語無視
# no_above: 使われてる文章の割合がno_above以上の場合無視

print("単語の圧縮後の数=", len(gensim_dic))  # 次元削減後の大きさ

X = []
Y = []
cat_names = []

for cat in os.listdir(root_dir):
    cat_dir = root_dir + "/" + cat
    if not os.path.isdir(cat_dir):
        continue
    cat_idx = len(cat_names)
    files = glob.glob(cat_dir + "/*.wakati")
    for path in files:
        # print(path)
        if path.find(".wakati") == -1:
            continue
        with open(path, "r") as f:
            text = f.read().strip()
            words = text.split(" ")
            vec = gensim_dic.doc2bow(words)
            # print(vec)
            dense = sparse.csc_matrix(matutils.corpus2csc([vec],
                                      num_terms=len(gensim_dic)).T[0])
            # print(dense)
            X.append(dense)
            Y.append(cat_idx)

# print(X)

# 単語辞書の作成
if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    json.dump(gensim_dic.token2id, open(dic_file, "w"))

print(X)
json.dump({"X": X, "Y": Y}, open(data_file, "w"))
