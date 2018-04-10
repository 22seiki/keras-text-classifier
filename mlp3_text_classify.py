from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation, metrics
import json

# max_words = 67395  # 入力単語数
nb_classes = 3     # 3カテゴリを分類

batch_size = 64
nb_epoch = 20


# MLPのモデルを生成
def build_model():
    global max_words
    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    return model

# データを読み込み
data = json.load(open("./text/data.json"))
# print('data: {}'.format(data))
# data = json.load(open("./newstext/data.json"))
X = data["X"]   # テキストを表すデータ
Y = data["Y"]   # カテゴリデータ
max_words = len(X[0])
# print('X: {}, Y: {}'.format(X, Y))
# 学習
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
Y_train = np_utils.to_categorical(Y_train, nb_classes)
print(len(X_train), len(Y_train))
model = KerasClassifier(
    build_fn=build_model,
    nb_epoch=nb_epoch,
    batch_size=batch_size
)
# print('X_train: {}, Y_train: {}'.format(X_train, Y_train))
model.fit(X_train, Y_train)

# 予測
y = model.predict(X_test)
ac_score = metrics.accuracy_score(Y_test, y)
cl_report = metrics.classification_report(Y_test, y)
print(" 正解率=", ac_score)
print(" レポート=\n", cl_report)
