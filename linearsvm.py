from sklearn.datasets import load_digits
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn import cross_validation
import json

# データの読み込み
data = json.load(open("./text/data_svm.json"))
X = data["X"]   # テキストを表すデータ
Y = data["Y"]   # カテゴリデータ
print("データ数 =", len(X))
train_x, test_x, train_y, test_y = train_test_split(X, Y)
clf = LinearSVC()
scores = cross_validation.cross_val_score(clf, X, Y, cv=10)
print(scores)
ave = sum(scores) / len(scores)
print(ave)

"""
# one-versus-the-restによる識別
estimator = SVC(C=1.0, kernel='linear', gamma=0.01)
classifier = OneVsRestClassifier(estimator)
classifier.fit(X, Y)
pred_y = classifier.predict(X)
cl_report = metrics.classification_report(Y, pred_y)
print(cl_report)

# one-versus-the-oneによる識別（デフォルト）
pred_y2 = clf.predict(X)
cl_report = metrics.classification_report(Y, pred_y2)
print(cl_report)

print('One-versus-the-rest: {:.5f}'
      .format(metrics.accuracy_score(test_y, pred_y)))
print('One-versus-one: {:.5f}'
      .format(metrics.accuracy_score(test_y, pred_y2)))"""
