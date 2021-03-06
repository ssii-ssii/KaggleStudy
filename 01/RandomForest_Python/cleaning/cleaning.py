# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pylab as P
import csv
from sklearn.ensemble import RandomForestClassifier 

#データの読み込み
train_df = pd.read_csv('../../data/train.csv',header=0)
test_df = pd.read_csv('../../data/test.csv',header=0)


train_df = train_df.fillna(-1)
test_df = test_df.fillna(-1)

train_df['Gender'] = train_df['Sex'].map( {'female': 0, 'male':1} ).astype(int)
test_df['Gender'] = test_df['Sex'].map( {'female': 0, 'male':1} ).astype(int)

train_df['Port'] = train_df['Embarked'].map( {'C': 1, 'Q':2, 'S':3, -1:0} ).astype(int)
test_df['Port'] = test_df['Embarked'].map( {'C': 1, 'Q':2, 'S':3, -1:0} ).astype(int)

##年齢の欠損値を中央値で代替する
##すべての要素が0の2行3列の"median_ages"行列をつくる
train_median_ages = np.zeros((2,3))
test_median_ages = np.zeros((2,3))

##上で作製したmedian_agesの各要素に、性別、クラス別の年齢中央値を入力する
for i in range(0, 2):
    for j in range(0, 3):
        train_median_ages[i,j] = train_df[(train_df['Gender'] == i) & (train_df['Pclass'] == j+1) & (test_df['Age'] != -1)]['Age'].median()
        test_median_ages[i,j] = test_df[(test_df['Gender'] == i) & (test_df['Pclass'] == j+1) & (test_df['Age'] != -1)]['Age'].median()

train_df['AgeFill'] = train_df['Age']
test_df['AgeFill'] = test_df['Age']

##AgeFillの欠損箇所に、median_agesを入力する
##pandasのloc関数（locで条件付けられている要素の、AgeFillのみを抽出し、そこに中央値（i,j）を使う
##http://oceanmarine.sakura.ne.jp/sphinx/group/group_pandas.html#id75
for i in range(0, 2):
    for j in range(0, 3):
        train_df.loc[ (train_df.Age.isnull()) & (train_df.Gender == i) & (train_df.Pclass == j+1), 'AgeFill'] = train_median_ages[i,j]
        test_df.loc[ (test_df.Age.isnull()) & (test_df.Gender == i) & (test_df.Pclass == j+1), 'AgeFill'] = test_median_ages[i,j]

##Fareの欠損値を中央値で代替する
train_df['FareFill'] = train_df['Fare']
train_df['FareFill'][train_df['FareFill'] == -1] = test_df['Fare'][train_df['FareFill'] != -1].median()

test_df['FareFill'] = test_df['Fare']
test_df['FareFill'][test_df['FareFill'] == -1] = test_df['Fare'][train_df['FareFill'] != -1].median()

##Embarkedの欠損値を最頻値で代替する
train_df['PortFill'] = train_df['Port']
test_df['PortFill'] = test_df['Port']

train_df.loc[(train_df.Port == 0), 'PortFill'] = train_df['Port'].median()
test_df.loc[(test_df.Port == 0), 'PortFill'] = test_df['Port'].median()


##不要なデータを落とす
##Name,Ticket,Cabin,Parchは、因果関係が不明なため
##Age,Fare,Sex,Embarked,PassengerIdは、Agefill,Gender,Portに代替し不要なため
train_df = train_df.drop(['Name','Ticket','Cabin','Age','Sex','Fare','Embarked','PassengerId','Port','PortFill','Parch'],axis=1)
test_df = test_df.drop(['Name','Ticket','Cabin','Age','Sex','Fare','Embarked','PassengerId','Port','PortFill','Parch'],axis=1)

##クリーン後の2次データをCSVで出力する
train_df.to_csv('train_cln.csv')
test_df.to_csv('test_cln.csv')

#データの読み込み
train_mng_df = pd.read_csv('train_cln.csv',index_col=0, header=0)
test_mng_df = pd.read_csv('test_cln.csv',index_col=0, header=0)

print train_mng_df.info()
print test_mng_df.info()