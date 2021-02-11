from PyQt5.QtWidgets import *

def set_Month_QtableWidget(monthqtw, infolist):

    sn = QTableWidgetItem(infolist[0])
    div = QTableWidgetItem(str(infolist[1]))
    itemlist = [sn, div]
    r = 0
    for r in range(0,100):
        if monthqtw.item(r,0) != None:
            if monthqtw.item(r, 0).text() == itemlist[0].text():  # if exists already input stockname, update
                break
            else:
                r += 1
        elif monthqtw.item(r, 0) == "":
            break
        else:
            break
    if r >= 8:
        monthqtw.insertRow(r)
    for i in range(0, len(itemlist)):
        monthqtw.setItem(r,i,itemlist[i])

def get_Monthly_dividend_sum(monthqtw):
    div_sum = 0.0
    for r in range(0,100):
        if monthqtw.item(r,1) != None:
            div_sum += float(monthqtw.item(r,1).text())
        else:
            break
    return div_sum

def set_getDetailSummary_QTableWidget(main):
    divsum_list = []
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_1))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_2))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_3))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_4))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_5))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_6))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_7))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_8))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_9))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_10))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_11))
    divsum_list.append(get_Monthly_dividend_sum(main.tableWidget_12))

    for c in range(0, len(divsum_list)):
        main.tableWidget_DetailSummary.setItem(0,c,QTableWidgetItem(str(divsum_list[c])))

def clear_getDetail_QTableWidget(main):
    main.tableWidget_1.clear()
    main.tableWidget_2.clear()
    main.tableWidget_3.clear()
    main.tableWidget_4.clear()
    main.tableWidget_5.clear()
    main.tableWidget_6.clear()
    main.tableWidget_7.clear()
    main.tableWidget_8.clear()
    main.tableWidget_9.clear()
    main.tableWidget_10.clear()
    main.tableWidget_11.clear()
    main.tableWidget_12.clear()

def set_getDetail_QTableWidget(main, div_months, infolist): #infolist = [stockname, dividend_lastest]
    print("set_Detail_Month")
    r = 0
    for month in div_months:
        if month == '01':
            set_Month_QtableWidget(main.tableWidget_1, infolist)
        elif month == '02':
            set_Month_QtableWidget(main.tableWidget_2, infolist)
        elif month == '03':
            set_Month_QtableWidget(main.tableWidget_3, infolist)
        elif month == '04':
            set_Month_QtableWidget(main.tableWidget_4, infolist)
        elif month == '05':
            set_Month_QtableWidget(main.tableWidget_5, infolist)
        elif month == '06':
            set_Month_QtableWidget(main.tableWidget_6, infolist)
        elif month == '07':
            set_Month_QtableWidget(main.tableWidget_7, infolist)
        elif month == '08':
            set_Month_QtableWidget(main.tableWidget_8, infolist)
        elif month == '09':
            set_Month_QtableWidget(main.tableWidget_9, infolist)
        elif month == '10':
            set_Month_QtableWidget(main.tableWidget_10, infolist)
        elif month == '11':
            set_Month_QtableWidget(main.tableWidget_11, infolist)
        elif month == '12':
            set_Month_QtableWidget(main.tableWidget_12, infolist)

