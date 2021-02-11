from StockInformation import *

if __name__ == "__main__":
    totalcount = len(stocks_code)
    cnt = 0
    for sc in stocks_code:
        stockcode = sc
        stockcountry = 'United States'
        if selectDB_exist_dividend_hist(stockcode, stockcountry) == False:
            print("insert")
            print(stockcode)
            insertDB_dividend_hist(stockcode, stockcountry)
        else:
            print(stockcode)
            print("exists")
        cnt +=1
        print("progress..." + str(cnt) + " / " + str(totalcount))