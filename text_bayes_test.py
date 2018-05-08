from text_bayes import BayesianFilter
import pickle
import os

bf = BayesianFilter()
# テキストを学習
persons = ['夏目漱石', '太宰治', '芥川龍之介']
sakuhin_count = {}
sakuhin_sum = {}
for person in persons:
    person_dir = "./text/" + person
    sakuhin_count[person] = 0  # 作品数を数えるため
    sakuhin_sum[person] = 0  # 作品数の合計
    # ディレクトリ内の作品数の合計を数える
    for sakuhin in os.listdir(person_dir):
        sakuhin_sum[person] += 1
    # print("作品数:", sakuhin_sum[person])
    for sakuhin in os.listdir(person_dir):
        sakuhin_count[person] += 1
        sakuhin_file = person_dir + "/" + sakuhin
        if sakuhin_file.find(".wakati") != -1:
            continue
        print(person, sakuhin)  # 経過を表示するため
        if sakuhin_count[person] < (sakuhin_sum[person] / 2):
            try:
                # 青空文庫のShift_JISファイルを読み込む
                bindata = open(sakuhin_file, "rb").read()
                text = bindata.decode("shift_jisx0213")
                bf.fit(text, person)  # 前半は学習させる
            except:
                print("[error]", sakuhin_file)
                continue
print("OK")

# 機械学習したモデルをバイナリファイルに変換
f = open('bayes.binaryfile', 'wb')
pickle.dump(bf, f)
f.close
