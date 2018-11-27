import pandas as pd
import numpy as np
import os


from flask import Flask,request,redirect,url_for,render_template
from sklearn import preprocessing
from openpyxl import Workbook,load_workbook
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor,MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix,mean_squared_error
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= os.path.realpath('.')


@app.route('/uploader', methods = ['POST'])
def uploader():
    target=os.path.join(app.config['UPLOAD_FOLDER'], 'data/')
    if not os.path.isdir(target):
             os.mkdir(target)

    for f in request.files.getlist("file"):
        filename="data-train.xlsx"
        destination="".join([target,filename])
        f.save(destination)
        url=str(destination)
        data = pd.read_excel(url,skiprows=4,sheet_name="Iklim")
        input = data[['Curah Hujan','Kecepatan Angin','Suhu']]
        minmax = preprocessing.MinMaxScaler(feature_range=(0,1))
        hasil1 = minmax.fit_transform(input)
        df1=pd.DataFrame(hasil1)

        data2 = pd.read_excel(url,skiprows=4,sheet_name="Produksi")
        target = data2[['Hasil per Ton']]
        minmax = preprocessing.MinMaxScaler(feature_range=(0,1))
        hasil2 = minmax.fit_transform(target)
        df2=pd.DataFrame(hasil2)

        norm_path = "data/normalisasi.xlsx"
        writer = pd.ExcelWriter(norm_path,engine='xlsxwriter')
        data_input = df1
        data_target = df2
        data_input.to_excel(writer, sheet_name="preprocessing", header=False, index=False,startcol=0 )
        data_target.to_excel(writer, sheet_name="preprocessing",header=False, index=False,startcol=3)
        writer.save()

        input_normalisasi = pd.read_excel(norm_path,sheet_name="preprocessing",usecols=[0,1,2], header=None, index=None)
        target_normalisasi= pd.read_excel(norm_path,sheet_name="preprocessing",usecols=[3],header=None,index=None)
        datainput = input_normalisasi.shape[0]
        datatarget = target_normalisasi.shape[0]

        j= datainput
        k= datatarget
        l=1
        m=0
        baris1=0
        baris2=0
        A=1
        B=2
        C=3
        D=4

        proses = load_workbook(norm_path)
        writer = pd.ExcelWriter(norm_path,engine='openpyxl')
        writer.book=proses
        for x in range (0,j):
            hasil0= input_normalisasi.iloc[[x]]
            if l == A:
                A = A + 3
                hasil0.to_excel(writer,sheet_name='data_proses',index=False,header=False,startrow=baris1,startcol=0)

            elif l==B:
                B =B+3
                hasil0.to_excel(writer,sheet_name='data_proses',index=False,header=False,startrow=baris1,startcol=3)
            elif l==C:
                C = C+3
                hasil0.to_excel(writer,sheet_name='data_proses',index=False,header=False,startrow=baris1,startcol=6)
                baris1=baris1+1
            else:
                D=D+3
            l=l+1

        for y in range (0,k):
            hasil=target_normalisasi.iloc[[y]]
            m=m+1
            if m == 0:
                continue
            hasil.to_excel(writer,sheet_name='data_proses',index=False,header=False,startrow=baris2,startcol=9)
            baris2=baris2+1

        writer.save()


        return  render_template('index.html')

@app.route('/upload')
def upload():
     return  render_template('upload.html')


if __name__=="__main__":
    app.run(debug=True)
