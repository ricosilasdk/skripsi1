import pandas as pd
import numpy as np
import xlsxwriter
import os

from flask import Flask,request,redirect,url_for,render_template
from sklearn import preprocessing
from openpyxl import Workbook
from sklearn.preprocessing import MinMaxScaler
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
        data_input = hasil1
        data_target = hasil2
        df1.to_excel(writer, sheet_name="preprocessing", header=False, index=False,startcol=0 )
        df2.to_excel(writer, sheet_name="preprocessing",header=False, index=False,startcol=3)
        writer.save()

        input_normalisasi = pd.read_excel(norm_path,sheet_name="preprocessing",usecols=[0,1,2])
        target_normalisasi=pd.read_excel(norm_path,sheet_name="preprocessing",usecols=3)
        datatrain = input_normalisasi.shape[0]
        datates =  target_normalisasi.shape[0]

        j= datatrain
        k= datates
        l=1
        m=0
        baris1=0
        baris2=0
        A=1
        B=2
        C=3
        D=4
        proses=pd.ExcelWriter(norm_path,engine='xlsxwriter')
        for x in range (0,j):
            hasil=j.iloc [[x]]
            if l== A:
                A=A+3
                hasil.to_excel(proses,sheet_name=data_proses,startrow=baris1,startcol=0)
            elif l==B:
                B=B+3
                hasil.to_excel(proses,sheet_name=data_proses,startrow=baris1,startcol=3)
            elif l==C:
                C=C+3
                hasil.to_excel(proses,sheet_name=data_proses,startrow=baris1,startcol=6)
                baris1=baris1+1
            else:
             D= D+3
            l=l+1
            endif
        endfor


        return  render_template('index.html')


@app.route('/upload')
def upload():
     return  render_template('upload.html')


if __name__=="__main__":
    app.run(debug=True)
