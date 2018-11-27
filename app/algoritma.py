import pandas as pd

from sklearn.neural_network import MLPRegressor,MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix,mean_squared_error
from sklearn.model_selection import train_test_split,KFold,cross_val_score,GridSearchCV

import numpy as np


# Read the dataset from csv fiel using pandas library
url='data/normalisasi.xlsx'
datainput=pd.read_excel(url,sheet_name="data_proses",header=None,index=None,usecols=[0,1,2,3,4,5,6,7,8])
datatarget=pd.read_excel(url,sheet_name="data_proses",header=None,index=None,usecols=[9])

shape=datainput.shape[0]
jml_train=shape-4
datatrain= datainput[0:jml_train]
targettrain=datatarget[0:jml_train]

validata= datainput[(jml_train-4):(jml_train)]
valitarget= datatarget[(jml_train-4):(jml_train)]
val_target=valitarget.as_matrix()
datatest=datainput[jml_train:shape]
targettest=datatarget[jml_train:shape]
target_test=targettest.as_matrix()

mlp=MLPRegressor(hidden_layer_sizes=(3,3,3), max_iter=1000,random_state=10,activation='relu',solver='adam',learning_rate_init=0.02,
                 learning_rate='constant')
mlp.fit(datatrain,targettrain.values.ravel())
hasil_validasi_train=mlp.predict(validata)
akurasi_rmse_train=mean_squared_error(val_target,hasil_validasi_train)

hasil_prediksi_test=mlp.predict(datatest)
akurasi_rmse_test=mean_squared_error(target_test,hasil_prediksi_test)





