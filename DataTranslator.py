from PyQt5.QtWidgets import *
import pandas as pd

def QTableWidget_To_DataFrame(qtw): #qtablewidget
    columns_name = ['StockCode','StockName','CurrentPrice','YearDividend','MyPrice','MyQuantity','Sum_MyPrice','Sum_YearDividend','Rate_Dividend','Country']
    df = pd.DataFrame(columns= columns_name)
    for r in range(0,100):
        if qtw.item(r,0) != None:
            datarow = []
            for c in range(0, len(columns_name)):
                datarow.append(qtw.item(r,c).text())
            df.loc[r] = datarow
        else:
            break
    return df

def DataFrame_To_QTableWidget(df, qtw): #set dataframe in QTableWidget
    rownum = df.shape[0]
    colnum = df.shape[1]
    dfarray = df.values
    for r in range(0,rownum):
       for c in range(0,colnum):
           qwitem = QTableWidgetItem(str(dfarray[r][c]))
           qtw.setItem(r,c,qwitem)