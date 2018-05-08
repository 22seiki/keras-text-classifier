import os
import glob
import json
import sys
import numpy as np

root_dir = "./text"
dic_file = root_dir + "/word-dic_svm.json"
data_file = root_dir + "/data_svm.json"
data_file_min = root_dir + "/data-mini_svm.json"

frq = {}  # 特徴量を格納
wd2idx = {}  # 文字ごとのIDを格納
idx2wd = {}  # IDごとに文字を格納
idx2frq = {}  # ID毎の頻出率を格納

# 語句を区切ってIDに変換する
word_dic = {"_MAX": 0}


def text_to_ids(text):
    text = text.strip()
    words = text.split(" ")
    result = []
    for n in words:
        n = n.strip()
        if n == "":
            continue
        if n not in word_dic:
            wid = word_dic[n] = word_dic["_MAX"]
            word_dic["_MAX"] += 1
            # print(wid, n)
        else:
            wid = word_dic[n]
        result.append(n)
    return result


# ファイルを読んで固定長シーケンスを返す
def file_to_ids(fname):
    with open(fname, "r") as f:
        text = f.read()
        return text_to_ids(text)


# 辞書に全部の単語を登録する
def register_dic():
    files = glob.glob(root_dir+"/*/*.wakati", recursive=True)
    # print(files)
    for i in files:
        file_to_ids(i)


# ファイル内の単語を数える
def count_file_freq(fname):
    cnt = [0 for n in range(len(idx2frq))]
    # print("cnt: {}".format(cnt))
    # print('length of cnt: {}'.format(len(cnt)))
    with open(fname, "r") as f:
        # print('fname: {}'.format(f))
        text = f.read().strip()
        # ids = idx2frq.values()
        wds = text_to_ids(text)
        # print('ids: {}'.format(ids))
        for wd in wds:
            try:
                if wd2idx[wd] in idx2frq:
                    # print(frq[wd], idx2frq[idx2wd[wd2idx[wd]]])
                    cnt[wd2idx[wd]] += 1  # 文字ごとのIDを格納
                # print(wd, frq[wd], idx2frq[wd2idx["自然"]])
                # sys.exit()
                # cnt[wid] = idx2frq[wid]
            except:
                print("Error", wd2idx[wd] in idx2frq)
                """print("wid={0}, cnt={1}, id={3}"
                      .format(wid, len(cnt), idx2frq[frq[wid]])"""
                # print(fname)
        # print("wid={0}, cnt={1}".format(idx2frq, len(cnt)))
    return cnt


# ジャンルごとにファイルを読み込む
def count_freq(limit=0):
    X = []
    Y = []
    Y_len = []
    max_words = word_dic["_MAX"]
    cat_names = []
    for cat in os.listdir(root_dir):
        cat_dir = root_dir + "/" + cat
        if not os.path.isdir(cat_dir):
            continue
        cat_idx = len(cat_names)
        # print(cat_idx)
        cat_names.append(cat)
        files = glob.glob(cat_dir + "/*.wakati")
        i = 0
        for path in files:
            # print(path)
            if path.find(".wakati") == -1:
                continue
            cnt = count_file_freq(path)
            X.append(cnt)
            Y.append(cat_idx)
            if cat_idx not in Y_len:
                Y_len.append(cat_idx)
            if limit > 0:
                if i > limit:
                    break
                i += 1
    return X, Y


# 特徴量を格納
def frq_words():
    for cat in os.listdir(root_dir):
        cat_dir = root_dir + "/" + cat
        if not os.path.isdir(cat_dir):
            continue
        files = glob.glob(cat_dir + "/*.wakati")
        i = 0
        for path in files:
            # print(path)
            if path.find(".wakati") == -1:
                continue
            with open(path, "r") as f:
                text = f.read().strip()
                words = text.split(" ")
                for n in words:
                    n = n.strip()
                    if n == "":
                        continue
                    if n in frq:
                        frq[n] += 1
                    else:
                        frq[n] = 1
    id = 0
    for k, v in sorted(frq.items(), key=lambda x: x[1], reverse=True):
        id += 1
        wd2idx[k] = id
        # print("wd2idx: {}".format(wd2idx[k]))
        idx2wd[id] = k
        idx2frq[id] = v

    idx2frq2 = idx2frq

    print(len(idx2frq2))

    for k in list(idx2frq2):
        if idx2frq2[k] <= 30:
            del(idx2frq[k])
        elif idx2frq2[k] >= len(idx2frq2)*0.3:
            del(idx2frq[k])

    print(len(idx2frq))


# 単語辞書の作成
if os.path.exists(dic_file):
    word_dic = json.load(open(dic_file))
else:
    register_dic()
    json.dump(word_dic, open(dic_file, "w"))

# ファイルごとの単語出現頻度のベクトルを作る
# テスト用に小規模のデータを用意
# X, Y = count_freq(20)
# json.dump({"X": X, "Y": Y}, open(data_file_min, "w"))
# 全ファイルを対象にデータを作成
frq_words()
X, Y = count_freq()

json.dump({"X": X, "Y": Y}, open(data_file, "w"))
print("ok")
