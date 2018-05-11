from gensim import corpora
import os
import glob

root_dir = "./text"

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

dictionary = corpora.Dictionary(wakati_ID)
# print(dictionary.token2id)

print("単語数=", len(dictionary))  # 次元の大きさ
"""
dictionary.filter_extremes(no_below=20, no_above=0.3)
# no_berow: 使われてる文章がno_berow個以下の単語無視
# no_above: 使われてる文章の割合がno_above以上の場合無視

print("単語の圧縮後の数=", len(dictionary))  # 次元削減後の大きさ"""

# 単語にIDを振ったものをテキストファイルに保存
dictionary.save_as_text('./wakati_gensim.txt')
