from text_bayes import BayesianFilter
import random
import os

bf = BayesianFilter()
# テキストを学習
persons = ['夏目漱石', '太宰治', '芥川龍之介']
sakuhin_count = {}
sakuhin_sum = {}
sakuhin_half = []
for person in persons:
    person_dir = "./text/" + person
    sakuhin_count[person] = 0  # 作品数を数えるため
    sakuhin_sum[person] = 0  # 作品数の合計
    results_half = []
    results_test = []
    # ディレクトリ内の作品数の合計を数える
    for sakuhin in os.listdir(person_dir):
        sakuhin_sum[person] += 1
    # print("作品数:", sakuhin_sum[person])
    for sakuhin in os.listdir(person_dir):
        # print(person, sakuhin)  # 経過を表示するため
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
                print("[error]", sakuhin_file, e)
                continue
        else:
            sakuhin_half.append(sakuhin_file)  # 後半はテストデータを格納
print("OK")

s = ""
while s.find("q") == -1:
    sakuhin_file_dir = random.choice(sakuhin_half)
    print(sakuhin_file_dir)  # 誰の作品かを判断するため　
    bindata = open(sakuhin_file_dir, "rb").read()
    text = bindata.decode("shift_jisx0213")
    pre, scorelist = bf.predict(text)  # 予測
    print("結果=", pre)
    print(scorelist)
    s = input()
