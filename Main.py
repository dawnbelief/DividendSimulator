import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import StockInformation as si
import os
import DataTranslator as ds
import pandas as pd
import DetailManager as dm
import CurrencyManager as cm

form_class = uic.loadUiType("DividendSimulator_Main.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # tablewidget_Main 기본 설정 : 셀 edit 가능 여부 설정 및 표시
        self.initilize_tableWidget_Main()

        # lineedit Widget에 종목코드 입력하면 사전순으로 입력 가능한 종목 list 출력
        self.lineEdit_StockSearch.textChanged.connect(self.view_SearchedStock)
        stocklist = si.get_StockList()
        completer = QCompleter(stocklist)
        self.lineEdit_StockSearch.setCompleter(completer)

        # lineedit Widget에 종목코드 입력하고 엔터 누르면 종목코드 -> tableWidget_Main 에 종목 정보 8개 입력 (사용자 값은 default)
        # * 입력값이 있어야 입력됨. 종목명으로 입력해도 코드 값으로 연결 시킬 수 있도록 기능 추가
        self.lineEdit_StockSearch.returnPressed.connect(self.set_searchedStock_Information)

        # tablewidget_Main에서 cell 클릭 했을 때, 변경 가능한 cell이라면 변경 후 enter 눌렀을 때 업데이트 한다.
        # myprice, myquantity, stockcode
        self.tableWidget_Main.cellClicked.connect(self.update_MainCell)

        # get Summary 버튼 누르면 summary 업데이트
        self.PushButton_Summary.clicked.connect(self.set_summary)

        # get Detail 버튼 누르면 detail 업데이트
        self.PushButton_Detail.clicked.connect(self.set_detail)

        # save
        self.PushButton_Save.clicked.connect(self.save_maintable)

        # load
        self.PushButton_Load.clicked.connect(self.load_maintable)

        # currency change
        self.PushButton_CurrencyChange.clicked.connect(self.change_currency_maintable)

        # Renew Today
        self.PushButton_RenewToday.clicked.connect(self.update_todayprice_maintable)

    def update_todayprice_maintable(self):
        print("Renew Today")
        currency = self.QLabel_Currency.text()
        print(currency)
        # CurrenctPrice, YearDividend, (option) MyPrice, Sum_MyPrice
        for r in range(0,100):
            if self.tableWidget_Main.item(r,0) != None:
                stockcode = self.tableWidget_Main.item(r,0).text()
                msinfo = si.get_MainStockInformation(stockcode, currency)
                currprice = msinfo[2]
                yeardividend = msinfo[3]
                myprice = msinfo[2] # Optional
                myquantity = float(self.tableWidget_Main.item(r,5).text())
                sum_myprice = round(myprice*myquantity, 2)
                sum_yeardividend = round(yeardividend*myquantity, 2)
                rd = round(msinfo[3] / msinfo[2] * 100, 2)

                currprice_new = QTableWidgetItem(str(currprice))
                yeardividend_new = QTableWidgetItem(str(yeardividend))
                myprice_new = QTableWidgetItem(str(myprice))
                summyprice_new = QTableWidgetItem(str(sum_myprice))
                sumyeardividend_new = QTableWidgetItem(str(sum_yeardividend))
                rate_dividend_new = QTableWidgetItem(str(rd))

                self.tableWidget_Main.setItem(r, 2, currprice_new)
                self.tableWidget_Main.setItem(r, 3, yeardividend_new)
                self.tableWidget_Main.setItem(r, 4, myprice_new)
                self.tableWidget_Main.setItem(r, 6, summyprice_new)
                self.tableWidget_Main.setItem(r, 7, sumyeardividend_new)
                self.tableWidget_Main.setItem(r, 8, rate_dividend_new)
            else:
                break

    def change_currency_maintable(self):
        print(self.QLabel_Currency.text())
        if self.QLabel_Currency.text() == 'USD':
            self.QLabel_Currency.setText('KRW')
            cm.ChangeCurrency_MainTable(self,'USD','KRW')

        elif self.QLabel_Currency.text() == 'KRW':
            self.QLabel_Currency.setText('USD')
            cm.ChangeCurrency_MainTable(self, 'KRW','USD')

    def load_maintable(self):
        print("load")
        file_load = QFileDialog.getOpenFileName(self, 'Load File', os.getenv('HOME'))
        if file_load[0] != '':
            df_load = pd.read_csv(file_load[0])
            ds.DataFrame_To_QTableWidget(df_load,self.tableWidget_Main)


    def save_maintable(self):
        print("save")
        df_qtw = ds.QTableWidget_To_DataFrame(self.tableWidget_Main)
        file_save = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
        if file_save[0] != '':
            df_qtw.to_csv(file_save[0], header=True, index=False)


    def set_detail(self):
        print("detail")
        dm.clear_getDetail_QTableWidget(self)
        for r in range(0,100):
            if self.tableWidget_Main.item(r,0) != None:
                stockcode = self.tableWidget_Main.item(r,0).text()
                stockcountry = si.stocks_dict_code_country[stockcode]
                localcurrency = self.QLabel_Currency.text()
                div_months = si.selectDB_get_dividend_lastyear_paymentdata_month(stockcode,stockcountry)
                div_latest = si.get_dividend_latest(stockcode,stockcountry)
                div_latest_new = cm.get_LocalCurrencyValue_NewStock(div_latest,localcurrency,stockcountry)
                stockname = self.tableWidget_Main.item(r,1).text()
                myquantity = float(self.tableWidget_Main.item(r,5).text())

                my_div_month = round(div_latest_new*myquantity,2)
                infolist = [stockname, my_div_month]
                print(infolist)
                dm.set_getDetail_QTableWidget(self, div_months, infolist)
                dm.set_getDetailSummary_QTableWidget(self)
            else:
                break

    def set_summary(self):
        tsp = 0.0
        tyd = 0.0
        for r in range(0,100):
            if self.tableWidget_Main.item(r,0) != None:
                smp = float(self.tableWidget_Main.item(r,6).text())
                tsp += smp
                syd = float(self.tableWidget_Main.item(r,7).text())
                tyd += syd
            else:
                break
        if tsp > 0.0:
            trd = round(tyd/tsp*100,2)
        else:
            trd = 0.0

        self.tableWidget_Summary.setItem(0,0,QTableWidgetItem(str(tsp)))
        self.tableWidget_Summary.setItem(0,1,QTableWidgetItem(str(tyd)))
        self.tableWidget_Summary.setItem(0,2,QTableWidgetItem(str(trd)))

    def initilize_tableWidget_Main(self):
        pass

    def update_MainCell(self, row, col):
        if self.tableWidget_Main.item(row,col) == None:
            pass
        else:
            if col == 4: #MyPrice
                self.update_MyPrice(row, col)
            if col == 5: #MyQuantity
                self.update_MyQuantity(row, col)
            if col == 0: #StockCode, 빈칸으로 만들면 삭제.
                self.delete_row(row,col)

    def delete_row(self,row,col):
        isdelete = self.tableWidget_Main.item(row, col).text()
        if isdelete == "":
            self.tableWidget_Main.removeRow(row)
            print("delete")

    def update_MyPrice(self,row,col):
        updatedMyPrice = self.tableWidget_Main.item(row,col).text()
        MyQuantity = float(self.tableWidget_Main.item(row,5).text())
        MyPrice = float(updatedMyPrice)
        YearDividend = float(self.tableWidget_Main.item(row,3).text())
        Sum_MyPrice = round(MyPrice*MyQuantity,2)
        Sum_YearDividend = round(YearDividend*MyQuantity,2)
        if Sum_MyPrice > 0.0:
            Rate_Dividend = round(Sum_YearDividend/Sum_MyPrice*100,2)
        else:
            Rate_Dividend = 0.0
        self.tableWidget_Main.setItem(row,6,QTableWidgetItem(str(Sum_MyPrice)))
        self.tableWidget_Main.setItem(row,7, QTableWidgetItem(str(Sum_YearDividend)))
        self.tableWidget_Main.setItem(row,8, QTableWidgetItem(str(Rate_Dividend)))

    def update_MyQuantity(self, row, col):
        updatedQuantity = self.tableWidget_Main.item(row,col).text()
        MyQuantity = float(updatedQuantity)
        MyPrice = float(self.tableWidget_Main.item(row,4).text())
        YearDividend = float(self.tableWidget_Main.item(row,3).text())
        Sum_MyPrice = round(MyPrice*MyQuantity,2)
        Sum_YearDividend = round(YearDividend*MyQuantity,2)
        self.tableWidget_Main.setItem(row,6,QTableWidgetItem(str(Sum_MyPrice)))
        self.tableWidget_Main.setItem(row,7, QTableWidgetItem(str(Sum_YearDividend)))


    #lineedit Widget에 종목코드 입력하면 tableWidget_Main에 정보 출력
    def view_SearchedStock(self):
        self.SearchedStock.setText(self.lineEdit_StockSearch.text())

    def set_searchedStock_Information(self):
        stockkey = self.SearchedStock.text()
        currency = self.QLabel_Currency.text()
        if stockkey in si.stocks_code or stockkey in si.stocks_name:
            #get_searchedStock_Information by stockkey
            #stockcode, stockname, currprice, dividend_year
            msinfo = si.get_MainStockInformation(stockkey,currency)
            print(msinfo)
            row = []
            stockcode = QTableWidgetItem(msinfo[0])
            stockname = QTableWidgetItem(msinfo[1])
            currprice = QTableWidgetItem(str(msinfo[2]))
            yeardividend = QTableWidgetItem(str(msinfo[3]))
            myprice = QTableWidgetItem(str(msinfo[2]))
            myquantity = QTableWidgetItem(str(0))
            sum_myprice = QTableWidgetItem(str(0.0))
            sum_yeardividend = QTableWidgetItem(str(0.0))
            rd = round(msinfo[3]/msinfo[2]*100,2)
            rate_dividend = QTableWidgetItem(str(rd))
            stockcountry =  QTableWidgetItem(msinfo[4])
            row.append(stockcode)
            row.append(stockname)
            row.append(currprice)
            row.append(yeardividend)
            row.append(myprice)
            row.append(myquantity)
            row.append(sum_myprice)
            row.append(sum_yeardividend)
            row.append(rate_dividend)
            row.append(stockcountry)
            r = 0
            for r in range(0,100):
                if self.tableWidget_Main.item(r, 0) != None:
                    r +=1
                elif self.tableWidget_Main.item(r, 0) == "":
                    break
                else:
                    break
            print(self.tableWidget_Main.rowCount())
            if r >= self.tableWidget_Main.rowCount():
                self.tableWidget_Main.insertRow(r)
            for i in range(0,len(row)):
                self.tableWidget_Main.setItem(r, i, row[i])


    def get_SearchedStockCode(self):
        stockkey = self.lineEdit_StockSearch.text()
        return stockkey





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()