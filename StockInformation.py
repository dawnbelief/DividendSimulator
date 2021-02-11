import investpy
from TrieStruct import *
import sqlite3
import pandas as pd
from datetime import datetime
import CurrencyManager as cm

#initialization
stocks_usa = investpy.get_stocks('United States')
stocks_kor = investpy.get_stocks('South Korea')
stocks = pd.concat([stocks_usa, stocks_kor])

stocks_name_temp = list(stocks['name'])
stocks_code = list(stocks['symbol'])
stocks_country = list(stocks['country'])


stocks_name = []
for sc in stocks_name_temp:
    scu = sc.upper()
    stocks_name.append(scu)


stocks_dict_code_name = {name: value for name, value in zip(stocks_code,stocks_name)}
stocks_dict_name_code = {code: value for code, value in zip(stocks_name,stocks_code)}
stocks_dict_code_country = {country: value for country, value in zip(stocks_code,stocks_country)}


# 조회 가능한 종목 코드, 종목명 list 반환
def get_StockList():
    stocks_code_name_list = stocks_name + stocks_code
    stocks_code_name_list = sorted(stocks_code_name_list)
    return stocks_code_name_list

def get_MainStockInformation(stockkey,currencycode): # stockcode, stockname, currprice, dividend_year # price in USD/KRW currency
    stock_info = []
    result = []
    if stockkey in stocks_code:
        stockcode = stockkey
        stockname = stocks_dict_code_name.get(stockcode)

    elif stockkey in stocks_name:
        stockname = stockkey
        stockcode = stocks_dict_name_code.get(stockname)
    else:
        return

    stockcountry = stocks_dict_code_country.get(stockcode)
    stockinfo = investpy.get_stock_information(stockcode, stockcountry, as_json=False)
    currprice = list(stockinfo['Prev. Close'])[0]
    dividend_year = get_dividend_year(stockcode, stockcountry)

    print(currprice)
    currprice_new = cm.get_LocalCurrencyValue_NewStock(currprice, currencycode, stockcountry)
    print(currprice_new)

    print(dividend_year)
    dividend_year_new = cm.get_LocalCurrencyValue_NewStock(dividend_year, currencycode, stockcountry)
    print(dividend_year_new)

    result.append(stockcode)
    result.append(stockname)
    result.append(currprice_new)
    result.append(dividend_year_new)
    result.append(stockcountry)
    return result


def get_dividend_latest(stockcode, stockcountry):
    if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
        insertDB_dividend_hist(stockcode, stockcountry)

    con = sqlite3.connect("Stock_Dividend.db")
    cursor = con.cursor()
    select_sql = "SELECT dividend, type FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
    select_sql += " AND COUNTRY = '" + stockcountry + "'"
    select_sql += " order by date desc limit 1"
    print(select_sql)

    cursor.execute(select_sql)
    result_sql = cursor.fetchone()
    result_div = float(result_sql[0])
    result_type = str(result_sql[1])
    result = round(result_div, 3)

    if result_type == 'trailing_twelve_months':
        year_now = datetime.today().year
        select_sql = "SELECT count(*) FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
        select_sql += " AND COUNTRY = '" + stockcountry + "'"
        select_sql += " AND DATE > '" + str(year_now-1) + "' AND DATE < '" + str(year_now) + "'"
        cursor.execute(select_sql)
        result_sql = cursor.fetchone()
        result_cnt = float(result_sql[0])
        if result_cnt == 4: # quarterly
            result = round(result_div / 4, 3)
        if result_cnt == 2: # semi-annual
            result = round(result_div / 2, 3)

    return result


def get_dividend_year(stockcode, stockcountry):
    if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
        insertDB_dividend_hist(stockcode, stockcountry)

    con = sqlite3.connect("Stock_Dividend.db")
    cursor = con.cursor()
    select_sql = "SELECT dividend, type type FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
    select_sql += " AND COUNTRY = '" + stockcountry + "'"
    select_sql += " order by date desc limit 1"

    cursor.execute(select_sql)
    result_sql = cursor.fetchone()
    result_div = float(result_sql[0])
    result_type = str(result_sql[1])
    result = round(result_div, 3)
    if result_type == 'quarterly':
        result = round(result_div*4,3)
    if result_type == 'monthly':
        result = round(result_div*12,3)
    if result_type == 'semi_annual':
        result = round(result_div*2,3)

    return result


def selectDB_get_dividend_hist(stockcode, stockcountry):
    if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
        insertDB_dividend_hist(stockcode, stockcountry)


def selectDB_get_dividend_lastyear_paymentdata_month(stockcode, stockcountry):
    if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
        insertDB_dividend_hist(stockcode, stockcountry)

    con = sqlite3.connect("Stock_Dividend.db")
    cursor = con.cursor()
    lastyear = datetime.today().year-1
    select_sql = "SELECT distinct substr(PaymentDate, 6,2) FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
    select_sql += " AND COUNTRY = '" + stockcountry + "'"
    select_sql += " AND DATE < '" + str(lastyear-1) + "'"
    select_sql += " order by date desc"
    select_sql += " limit 12"
    print(select_sql)
    cursor.execute(select_sql)
    result_sql = list(cursor.fetchall())
    result = []
    for r in result_sql:
        result.append(r[0])
    print(result)
    return result



def selectDB_get_dividend_lastyear_sum(stockcode, stockcountry):
    if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
        insertDB_dividend_hist(stockcode, stockcountry)

    con = sqlite3.connect("Stock_Dividend.db")
    cursor = con.cursor()
    lastyear = datetime.today().year-1
    select_sql = "SELECT sum(dividend) FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
    select_sql += " AND COUNTRY = '" + stockcountry + "'"
    select_sql += " AND DATE LIKE '%" + str(lastyear) + "%'"

    cursor.execute(select_sql)
    result = float(cursor.fetchone()[0])
    return result




def selectDB_exist_dividend_hist(stockcode, stockcountry):
    con = sqlite3.connect("Stock_Dividend.db")
    cursor = con.cursor()
    select_sql = "SELECT * FROM Stock_Dividend WHERE STOCKCODE = '" + stockcode + "'"
    select_sql += " AND COUNTRY = '" + stockcountry + "'"
    cursor.execute(select_sql)

    print(select_sql)
    print(cursor.fetchone())
    if cursor.fetchone() == None:
        result = False
    else:
        result = True

    con.close()
    return result

def insertDB_dividend_hist(stockcode, stockcountry):

    try:
        con = sqlite3.connect("Stock_Dividend.db")
        cursor = con.cursor()
        div = investpy.stocks.get_stock_dividends(stockcode, stockcountry)
        Dividend = list(div['Dividend'])
        Date = list(div['Date'])
        Type = list(div['Type'])
        PaymentDate = list(div['Payment Date'])

        for i in range(0, len(Dividend)):
            # INSERT INTO Stock_Dividend VALUES ('AAPL',1.00,'2020-01-01','YEAR','2020-01-14')
            insert_sql = "INSERT INTO Stock_Dividend "
            insert_sql += "(StockCode, Dividend, Date, Type, PaymentDate, Country) "
            insert_sql += "VALUES ('" + stockcode + "', " + str(Dividend[i]) + ",'" + str(Date[i]) + "','"
            insert_sql += str(Type[i]) + "','" + str(PaymentDate[i]) + "','" + stockcountry + "')"
            print(insert_sql)
            cursor.execute(insert_sql)

        cursor.execute("commit")
        con.close()

    except (RuntimeError, ConnectionError):

        Dividend = [0.0]
        Date = ['1000-01-01']
        Type = ['None']
        PaymentDate = ['1000-01-01']

        for i in range(0, len(Dividend)):
            # INSERT INTO Stock_Dividend VALUES ('AAPL',1.00,'2020-01-01','YEAR','2020-01-14')
            insert_sql = "INSERT INTO Stock_Dividend "
            insert_sql += "(StockCode, Dividend, Date, Type, PaymentDate, Country) "
            insert_sql += "VALUES ('" + stockcode + "', " + str(Dividend[i]) + ",'" + str(Date[i]) + "','"
            insert_sql += str(Type[i]) + "','" + str(PaymentDate[i]) + "','" + stockcountry + "')"
            print(insert_sql)
            cursor.execute(insert_sql)

        cursor.execute("commit")
        con.close()



