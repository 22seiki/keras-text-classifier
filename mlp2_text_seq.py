import os
import glob
import json

root_dir = "./text"
dic_file = root_dir + "/word-dic.json"
data_file = root_dir + "/data.json"
data_file_min = root_dir + "/data-mini.json"

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
            print(wid, n)
        else:
            wid = word_dic[n]
        result.append(wid)
    return result


# ファイルを読んで固定長シーケンスを返す
def file_to_ids(fname):
    with open(fname, "r") as f:
        text = f.read()
        return text_to_ids(text)


# 辞書に全部の単語を登録する
def register_dic():
    files = glob.glob(root_dir+"/*/*.wakati", recursive=True)
    print(files)
    for i in files:
        file_to_ids(i)


# ファイル内の単語を数える
def count_file_freq(fname):
    # print("word_dic: {}".format(word_dic["_MAX"]))
    cnt = [0 for n in range(word_dic["_MAX"])]
    # print("cnt: {}".format(cnt))
    # print('length of cnt: {}'.format(len(cnt)))
    with open(fname, "r") as f:
        # print('fname: {}'.format(f))
        text = f.read().strip()
        ids = text_to_ids(text)
        # print('ids: {}'.format(ids))
        for wid in ids:
            # print("index: {}".format(len(ids)))
            # print('cnt[wid]: {}'.format(cnt))
            try:
                cnt[wid] += 1
            except:
                print("Error")
                print(text)
    return cnt


# ジャンルごとにファイルを読み込む
def count_freq(limit=0):
    X = []
    Y = []
    max_words = word_dic["_MAX"]
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
X, Y = count_freq()
json.dump({"X": X, "Y": Y}, open(data_file, "w"))
print("ok")
