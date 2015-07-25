# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pylab as P
import csv
from sklearn.ensemble import RandomForestClassifier 
import matplotlib.pyplot as plt

#データの読み込み
train_mng_df = pd.read_csv('munging/train_mng.csv',index_col=0, header=0)
test_mng_df = pd.read_csv('munging/test_mng.csv',index_col=0, header=0)

##sklearn packageではpandasを扱えないので、最後にnumpyarrayに戻す
train_mng_data = train_mng_df.values
test_mng_data = test_mng_df.values

#randomforestの適用
#https://www.kaggle.com/c/titanic/details/getting-started-with-random-forests
##モデル(forest_test)の定義とパラメータの入力(n_estimators = 100)
forest_test = RandomForestClassifier(n_estimators = 100)
##モデルに訓練データtrain_data[0::,1::]と、訓練ラベルtrain_data[0::,0](Survived)を入れる
forest_test = forest_test.fit(train_mng_data[0::,1::],train_mng_data[0::,0])
##上で学習されたモデルにテストデータを入力し、予測結果をoutputとする
output = forest_test.predict(test_mng_data)
#特徴量の重要度をグラフ表示
features = pd.Series(forest_test.feature_importances_,index = test_mng_df.columns)
features.plot(kind='barh')
plt.title('Randomforest feature importances')
plt.show()
plt.savefig("feature_importances.png")

##予測結果を入れるためのCSVファイルを作る
predictions_file = open('../data/MyFirstForest.csv', "wb")
#CSVファイルをpythonで開く
open_file_object = csv.writer(predictions_file)
#列名を書き込む
open_file_object.writerow(["Survived"])
#テストデータのPassengerIdと予測データを入れる
open_file_object.writerows(zip(output))
#CSVファイルを閉じる
predictions_file.close()
