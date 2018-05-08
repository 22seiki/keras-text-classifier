import pickle
import os
import random

f = open('bayes.binaryfile', 'rb')
bf = pickle.load(f)

persons = ['夏目漱石', '太宰治', '芥川龍之介']
sakuhin_count = {}
sakuhin_sum = {}
author_count = {}
author_sum = {}
for person in persons:
    person_dir = "./text/" + person
    sakuhin_count[person] = 0  # 作品数を数えるため
    sakuhin_sum[person] = 0  # 作品数の合計
    author_count[person] = 0
    author_sum[person] = 0
    # ディレクトリ内の作品数の合計を数える
    for sakuhin in os.listdir(person_dir):
        sakuhin_sum[person] += 1
    # print("作品数:", sakuhin_sum[person])
    for sakuhin in os.listdir(person_dir):
        sakuhin_count[person] += 1
        sakuhin_file = person_dir + "/" + sakuhin
        if sakuhin_file.find(".wakati") != -1:
            continue
        if sakuhin_count[person] > (sakuhin_sum[person] / 2):
            # print(sakuhin_file)  # 誰の作品かを判断するため
            author_sum[person] += 1
            bindata = open(sakuhin_file, "rb").read()
            text = bindata.decode("shift_jisx0213")
            # sakuhin_half.append(sakuhin_file)  # テストデータの格納
            pre, scorelist = bf.predict(text)  # 予測
            # print("結果=", pre)
            # print(scorelist)
            if pre in person:
                print('[correct]', sakuhin_file)  # 誰の作品かを判断するため
                author_count[person] += 1
            else:
                print('[miss]:', sakuhin_file)
            if author_sum[person] == 10:
                break
    # print('{0}:{1}/{2}'.format(person, author_count, author_sum))
print("ok")

sum_correct = 0
sum_sakuhin = 0
for person in persons:
    pro = author_count[person] / author_sum[person]
    print('{0}:{1}/{2} 正答率 = {3}'
          .format(person, author_count[person], author_sum[person], pro))
    sum_correct += author_count[person]
    sum_sakuhin += author_sum[person]

print("結果\t:{0}/{1} 全体の正解率 = {2}"
      .format(sum_correct, sum_sakuhin, sum_correct/sum_sakuhin))
