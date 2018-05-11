from gensim import corpora, matutils
import os
import glob
import json

root_dir = "./text"
dic_file = root_dir + "/word-dic_svm.json"
data_file = root_dir + "/data_gensim_svm.json"

dictionary = corpora.Dictionary.load_from_text("./wakati_gensim.txt")

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
        print(path)
        if path.find(".wakati") == -1:
            continue
        with open(path, "r") as f:
            text = f.read().strip()
            words = text.split(" ")
            vec = dictionary.doc2bow(words)
            dense = list(matutils.corpus2csc([vec],
                         num_terms=len(dictionary)).T[0])
            X.append(dense)
            Y.append(cat_idx)

json.dump({"X": X, "Y": Y}, open(data_file, "w"))
