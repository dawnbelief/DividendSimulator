import investpy as ip
from datetime import datetime
from datetime import timedelta
from PyQt5.QtWidgets import *

codelist = ['USD','KRW']
namelist = ['united states','south korea']
currency_dict_name_code = {code: value for code, value in zip(namelist,codelist)}
currency_dict_code_name = {value: code for value, code in zip(codelist,namelist)}

def get_CurrentCurrencyExchange_initial(fromcur, tocur):
    cc = fromcur + "/" + tocur
    currdf = ip.get_currency_cross_information(currency_cross=cc)
    cnow = list(currdf['Prev. Close'])[0]
    return cnow

cnow_KRW_USD = get_CurrentCurrencyExchange_initial('KRW', 'USD')
cnow_USD_KRW = get_CurrentCurrencyExchange_initial('USD', 'KRW')
#print(cnow_KRW_USD) #1KRW by USD
#print(cnow_USD_KRW) #1USD by KRW
def get_CurrentCurrencyExchange(fromcur, tocur): # KRW, USD
    if fromcur == 'KRW' and tocur == 'USD':
        return cnow_KRW_USD
    elif fromcur == 'USD' and tocur == 'KRW':
        return cnow_USD_KRW
    else:
        return 1.0


def get_LocalCurrencyValue_NewStock(stockvalue,LocalCurrency,stockCountry): #LocalCurrency
    print("get_CurrentCurrencyValue")
    if stockCountry == currency_dict_code_name[LocalCurrency]:
        print("noexchange")
        return stockvalue
    else:
        print("exchange")
        if stockCountry == namelist[0]: #United States
           if LocalCurrency == 'KRW':
               cnow = cnow_USD_KRW
        else:
           if LocalCurrency == 'USD':
               cnow = cnow_KRW_USD
        return round(stockvalue*cnow,2)


def CurrencyExchange_QTableWidgetItem(qtwi, cnow):
    originvalue = float(qtwi.text())
    newvalue = round(originvalue*cnow,2)
    newqtwi = QTableWidgetItem(str(newvalue))
    return newqtwi


def ChangeCurrency_MainTable(main, fromcur, tocur):
    mainqwt = main.tableWidget_Main
    cnow = get_CurrentCurrencyExchange(fromcur, tocur)
    main.QLabel_Currency2.setText(str(cnow))
    for r in range(0,100):
        if mainqwt.item(r,0) != None:
            cp_new = CurrencyExchange_QTableWidgetItem(mainqwt.item(r,2),cnow)
            yd_new = CurrencyExchange_QTableWidgetItem(mainqwt.item(r,3),cnow)
            mp_new = CurrencyExchange_QTableWidgetItem(mainqwt.item(r,4),cnow)
            summp_new = CurrencyExchange_QTableWidgetItem(mainqwt.item(r,6),cnow)
            sumyd_new = CurrencyExchange_QTableWidgetItem(mainqwt.item(r,7),cnow)
            mainqwt.setItem(r, 2, cp_new)
            mainqwt.setItem(r, 3, yd_new)
            mainqwt.setItem(r, 4, mp_new)
            mainqwt.setItem(r, 6, summp_new)
            mainqwt.setItem(r, 7, sumyd_new)
        else:
            break
