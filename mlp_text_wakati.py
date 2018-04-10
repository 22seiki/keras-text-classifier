# coding: utf-8
from janome.tokenizer import Tokenizer
import os
import glob
import re


# 日本語を分かち書き
def tokenize(text):
    t = Tokenizer()
    # テキストの先頭にあるヘッダーとフッターを削除
    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本:', text)[0]
    text = text.strip()
    # ルビを削除
    text = text.replace('|', '')
    text = re.sub(r'<<.+?>> ', '', text)
    # テキスト内の脚注を削除
    text = re.sub(r'[#.+?]', '', text)
    # 一行ずつ処理
    lines = text.split("\r\n")
    results = []
    for line in lines:
        res = []
        tokens = t.tokenize(line)
        for tok in tokens:
            ps = tok.part_of_speech  # 品詞情報
            hinsi = ps.split(',')[0]
            if hinsi not in ['名詞', '動詞', '形容詞']:
                # res.append(bf)
                continue
            bf = tok.base_form  # 基本系
            if bf == "*" or bf == "":
                bf = tok.surface
            if bf == "" or bf == "\n":
                continue
            res.append(bf)
        l = " ".join(res)
        results.append(l)
        res.append("\n")
    return results

# 辞書データの作成
persons = ['夏目漱石', '太宰治', '芥川龍之介']
sakuhin_count = {}
sakuhin_sum = {}
for person in persons:
    person_dir = "./text/" + person
    sakuhin_count[person] = 0  # 作品数を数えるため
    sakuhin_sum[person] = 0  # 作品数の合計
    results_half = []
    results_test = []
    print(os.path.isfile("./"))
    # ディレクトリ内の作品数の合計を数える
    for sakuhin in os.listdir(person_dir):
        sakuhin_sum[person] += 1
    # print("作品数:", sakuhin_sum[person])
    for sakuhin in os.listdir(person_dir):
        # print(person, sakuhin)  # 経過を表示するため
        sakuhin_count[person] += 1
        sakuhin_file = person_dir + "/" + sakuhin
        # print(sakuhin_file)
        path_wakati = sakuhin_file + ".wakati"
        # print(path_wakati)
        if os.path.exists(path_wakati):
            continue
        if sakuhin_file.find(".wakati") != -1:
            continue
        if os.path.exists(sakuhin_file + ".wakati"):
            continue
        print(person, sakuhin)  # 経過を表示するため
        try:
            # 青空文庫のShift_JISファイルを読み込む
            bindata = open(sakuhin_file, "rb").read()
            text = bindata.decode("shift_jis")
            lines = tokenize(text)
            results_half += lines
            with open(path_wakati, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception as e:
            print("[error]", sakuhin_file, e)
            continue
        # ファイルへ保存
        # fname1 = "./text/" + person + "/" + person + "_half.wakati"
    print(person)

print("作品数:", sakuhin_count)
