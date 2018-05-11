import os
import glob
import json
import sys

root_dir = "./text"
dic_file = root_dir + "/word-dic_svm.json"
data_file = root_dir + "/data_svm.json"

frq = {}  # 特徴量を格納
wd2idx = {}  # 文字ごとのIDを格納
idx2wd = {}  # IDごとに文字を格納
idx2frq = {}  # ID毎の頻出率を格納


# テキストを単語に分ける
def text_to_wds(text):
    text = text.strip()
    words = text.split(" ")
    result = []
    for n in words:
        n = n.strip()
        if n == "":
            continue
        result.append(n)
    return result


# ファイル内の単語を数える
def count_file_freq(fname):
    cnt = [0 for n in range(len(idx2frq))]
    with open(fname, "r") as f:
        text = f.read().strip()
        wds = text_to_wds(text)
        for wd in wds:
            try:
                cnt[wd2idx[wd]] += 1  # 文字ごとのIDを格納
            except:
                print("Error:", wd)
    return cnt


# ジャンルごとにファイルを読み込む
def count_freq(limit=0):
    X = []
    Y = []
    cat_names = []
    for cat in os.listdir(root_dir):
        cat_dir = root_dir + "/" + cat
        if not os.path.isdir(cat_dir):
            continue
        cat_idx = len(cat_names)
        cat_names.append(cat)
        files = glob.glob(cat_dir + "/*.wakati")
        i = 0
        for path in files:
            print(path)
            if path.find(".wakati") == -1:
                continue
            cnt = count_file_freq(path)
            X.append(cnt)
            Y.append(cat_idx)
            if limit > 0:
                if i > limit:
                    break
                i += 1
    return X, Y


# 特徴量を格納
def frq_words():
    global t_count
    for cat in os.listdir(root_dir):
        cat_dir = root_dir + "/" + cat
        if not os.path.isdir(cat_dir):
            continue
        files = glob.glob(cat_dir + "/*.wakati")
        for path in files:
            if path.find(".wakati") == -1:
                continue
            t_count += 1
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
        idx2wd[id] = k
        idx2frq[id] = v

    print("単語数={}".format(len(frq)))

frq_words()

# 単語辞書の作成
if os.path.exists(dic_file):
    wd2idx = json.load(open(dic_file))
else:
    json.dump(wd2idx, open(dic_file, "w"))

# ファイルごとの単語出現頻度のベクトルを作る
# テスト用に小規模のデータを用意
# X, Y = count_freq(20)
# json.dump({"X": X, "Y": Y}, open(data_file_min, "w"))
# 全ファイルを対象にデータを作成
X, Y = count_freq()

json.dump({"X": X, "Y": Y}, open(data_file, "w"))
print("ok")
