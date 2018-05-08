from sklearn.datasets import load_digits
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import cross_validation, metrics
import json
from gensim import corpora, matutils
from sklearn import decomposition
import pylab as pl
import numpy as np

# データの読み込み
data = json.load(open("./text/data_svm.json"))
X = data["X"]   # テキストを表すデータ
Y = data["Y"]   # カテゴリデータ
# print(Y)

pca = decomposition.PCA(n_components=10)
pca.fit(X)
X = pca.transform(X)
# print(X)
train_x, test_x, train_y, test_y = train_test_split(X, Y)

# ハイパーパラメータの設定
C = 1.0
kernel = 'rbf'
gamma = 0.01

# one-versus-the-restによる識別
estimator = SVC(C=C, kernel=kernel, gamma=gamma)
classifier = OneVsRestClassifier(estimator)
classifier.fit(train_x, train_y)
pred_y = classifier.predict(test_x)
cl_report = metrics.classification_report(test_y, pred_y)
print(cl_report)

# one-versus-the-oneによる識別（デフォルト）
classifier2 = SVC(C=C, kernel=kernel, gamma=gamma)
classifier2.fit(train_x, train_y)
pred_y2 = classifier2.predict(test_x)
cl_report = metrics.classification_report(test_y, pred_y2)
print(cl_report)

print('One-versus-the-rest: {:.5f}'.format(accuracy_score(test_y, pred_y)))
print('One-versus-one: {:.5f}'.format(accuracy_score(test_y, pred_y2)))
