from binance.client import Client
from binance.enums import *
import json
from time import sleep
import sys
from PyQt5.QtWidgets import *
from threading import Thread
import ccxt
import tkinter
from datetime import datetime

global api_key
global api_secret
global wallet
global price
global longPos
global shortPos
global longVolume
global shortVolume
global longTime
global shortTime
global reverage
global Long
global Short
global binance
global position

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        gridUp = QGridLayout()
        gridMid = QGridLayout()
        grid.addLayout(gridUp, 1, 0)
        grid.addLayout(gridMid, 2, 0)

        btnStart = QPushButton("start", self)
        btnStart.clicked.connect(self.btnStartEvent)
        grid.addWidget(btnStart,0,0)

        label1 = QLabel('Price : ', self)
        gridUp.addWidget(label1, 0, 0)

        self.labelPrice = QLabel('', self)
        gridUp.addWidget(self.labelPrice, 0, 1)

        label2 = QLabel('Wallet : ', self)
        gridUp.addWidget(label2, 1, 0)

        self.labelWallet = QLabel('', self)
        gridUp.addWidget(self.labelWallet, 1, 1)

        label3 = QLabel('LONG', self)
        gridMid.addWidget(label3,0,1)

        label4 = QLabel('SHORT', self)
        gridMid.addWidget(label4,0,2)

        label5 = QLabel('Time', self)
        gridMid.addWidget(label5,1,0)

        self.labelLongTime = QLabel('',self)
        gridMid.addWidget(self.labelLongTime,1,1)

        self.labelShortTime = QLabel('',self)
        gridMid.addWidget(self.labelShortTime,1,2)

        label6 = QLabel('Entry', self)
        gridMid.addWidget(label6,2,0)

        self.labelLongPos = QLabel('',self)
        gridMid.addWidget(self.labelLongPos,2,1)

        self.labelShortPos = QLabel('',self)
        gridMid.addWidget(self.labelShortPos,2,2)

        label7 = QLabel('Volume', self)
        gridMid.addWidget(label7,3,0)

        self.labelLongVolume = QLabel('',self)
        gridMid.addWidget(self.labelLongVolume,3,1)

        self.labelShortVolume = QLabel('',self)
        gridMid.addWidget(self.labelShortVolume,3,2)

        label8 = QLabel('earn', self)
        gridMid.addWidget(label8,4,0)

        self.labelLongEarn = QLabel('',self)
        gridMid.addWidget(self.labelLongEarn,4,1)

        self.labelShortEarn = QLabel('',self)
        gridMid.addWidget(self.labelShortEarn,4,2)

        self.tb1 = QTextBrowser()
        self.tb1.setOpenExternalLinks(False)
        grid.addWidget(self.tb1,3,0)
        
        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def btnStartEvent(self):
        def runAuto():
            print('hello')
            global wallet
            global longPos
            global shortPos
            global longVolume
            global shortVolume
            global longTime
            global shortTime
            global reverage
            global Long
            global Short
            global binance
            global price
            global position
            price = getPrice()
            '''
            #back test code
            while (True):
                now = datetime.now()
                chai = price - getPrice()
                price = getPrice()
                self.labelPrice.setText(""+str(price)+"("+str(round(chai,2))+")")
                if Long:
                    try:
                        if (price - longPos)/longPos * reverage * 100 <= -3:

                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / LONG / loss / " + str(round((price - longPos)/longPos * longVolume * reverage,2)))
                            self.labelLongTime.setText('')
                            self.labelLongPos.setText('')
                            self.labelLongVolume.setText('')
                            self.labelLongEarn.setText('')
                            wallet += longVolume + (price - longPos)/longPos * longVolume * reverage
                            self.tb1.append(str(round((price - longPos) / longPos * longVolume * reverage, 2)) + " + " + str(round(longVolume,2)))
                            longPos = 0.0
                            Long = False
                            longTime = 60

                        if (price - longPos)/longPos * reverage * 100 >= 1:
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / LONG / earn / " + str(round((price - longPos)/longPos * longVolume * reverage, 2)))

                            wallet += longVolume + (price - longPos)/longPos * longVolume * reverage
                            self.tb1.append(str(round((price - longPos) / longPos * longVolume * reverage, 2)) + " + " + str(round(longVolume,2)))
                            longPos = 0.0
                            Long = False
                    except ZeroDivisionError:
                        pass

                if Short:
                    try:
                        if (shortPos - price)/shortPos * reverage * 100 >= 1:
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / SHORT / earn / " + str(round((shortPos - price)/shortPos * shortVolume * reverage, 2)))
                            wallet += shortVolume + (shortPos - price)/shortPos * shortVolume * reverage
                            self.tb1.append(str(round((shortPos - price) / shortPos * shortVolume * reverage,2)) + " + " + str(round(shortVolume,2)))
                            shortPos = 0.0
                            Short = False

                        if (shortPos - price)/shortPos * reverage * 100 <= -3:
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / SHORT / loss / " + str(round((shortPos - price)/shortPos * shortVolume * reverage, 2)))
                            self.labelShortTime.setText('')
                            self.labelShortPos.setText('')
                            self.labelShortVolume.setText('')
                            self.labelShortEarn.setText('')
                            wallet += shortVolume + (shortPos - price)/shortPos * shortVolume * reverage
                            self.tb1.append(str(round((shortPos - price) / shortPos * shortVolume * reverage, 2)) + " + " + str(round(shortVolume,2)))
                            shortPos = 0.0
                            Short = False
                            shortTime = 60
                    except ZeroDivisionError:
                        pass
                if not Long and longTime == 0:
                    longPos = price
                    longVolume = wallet * 0.1

                    self.labelLongVolume.setText(str(round(wallet*0.1,2)))
                    self.labelLongPos.setText(str(round(price,2)))
                    self.labelLongTime.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
                    wallet -= wallet * 0.1
                    Long = True

                if not Short and shortTime == 0:
                    print("short!!")
                    shortPos = price
                    shortVolume = wallet * 0.1
                    self.labelShortVolume.setText(str(round(wallet * 0.1, 2)))
                    self.labelShortPos.setText(str(round(price, 2)))
                    self.labelShortTime.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
                    wallet -= wallet * 0.1
                    Short = True
                if longTime > 0:
                    longTime -= 1
                    self.labelLongTime.setText(str(longTime))
                if shortTime > 0:
                    shortTime -= 1
                    self.labelShortTime.setText(str(shortTime))
                if Long and Short and longPos - price != 0 and shortPos - price != 0:
                    #(price - longPos)/longPos * longVolume * reverage
                    #(shortPos - price)/shortPos * shortVolume * reverage
                    self.labelLongEarn.setText(str(round((price - longPos)/longPos * longVolume * reverage,2)) + "(" + str(round((price - longPos)/longPos * reverage * 100,2)) + "%)")
                    self.labelShortEarn.setText(str(round((shortPos - price)/shortPos * shortVolume * reverage,2)) + "(" + str(round((shortPos - price)/shortPos * reverage * 100,2)) + "%)")
                    self.labelWallet.setText(str(round(wallet + (price - longPos)/longPos * longVolume * reverage + longVolume + (shortPos - price)/shortPos * shortVolume * reverage + shortVolume, 2)))
                if Long and not Short and longPos - price != 0:
                    self.labelLongEarn.setText(str(round((price - longPos)/longPos * longVolume * reverage,2)) + "(" + str(round((price - longPos)/longPos * reverage * 100,2)) + "%)")
                    self.labelWallet.setText(str(round(wallet + (price - longPos)/longPos * longVolume * reverage + longVolume + shortVolume, 2)))
                if Short and not Long and shortPos - price != 0:
                    self.labelShortEarn.setText(str(round((shortPos - price)/shortPos * shortVolume * reverage,2)) + "(" + str(round((shortPos - price)/shortPos * reverage * 100,2)) + "%)")
                    self.labelWallet.setText( str(round(wallet + longVolume + (shortPos - price)/shortPos * shortVolume * reverage + shortVolume, 2)))
                else:
                    self.labelWallet.setText(str(round(wallet, 2)))

                sleep(1)
                '''
            sleep(1)
            chai = price - getPrice()
            switcher = True
            leverage = client.futures_change_leverage(symbol='BTCUSDT', leverage=100)
            if chai < 0:
                switcher = False
            while(True):
                price = getPrice()
                wallet = getBalance()
                position = getPositionInfo()
                if float(position['positionAmt']) > 0:
                    Long = True
                    Short = False
                elif float(position['positionAmt']) < 0:
                    Long = False
                    Short = True
                else:
                    Long = False
                    Short = False
                self.labelPrice.setText(str(round(price,2)))
                now = datetime.now()

                if switcher and not Long:
                    longOrder()
                    self.labelLongTime.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
                    Long = True

                if not switcher and not Short:
                    shortOrder()
                    self.labelShortTime.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
                    Short = True

                if Long:
                    pnl = getPNL(Long)
                    if float(position['positionAmt']) == 0:
                        longOrder()
                    self.labelLongEarn.setText(position['unRealizedProfit'] + "(" + str(pnl) + "%)")
                    self.labelLongPos.setText(position['entryPrice'])
                    self.labelLongVolume.setText(str(float(position['positionAmt']) * price))
                    try:
                        if pnl <= -1.0:
                            print('longClose PNL up')
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / LONG / loss / " + position['unRealizedProfit'])
                            self.labelLongTime.setText('')
                            self.labelLongPos.setText('')
                            self.labelLongVolume.setText('')
                            self.labelLongEarn.setText('')
                            Long = False
                            switcher = False
                            longClose()

                        if pnl >= 1.0:
                            print('longClose PNL up')
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / LONG / earn / " + position['unRealizedProfit'])
                            Long = False
                            longClose()
                    except:
                        pass

                if Short:
                    pnl = getPNL(Long)
                    if float(position['positionAmt']) == 0:
                        shortOrder()
                    self.labelShortEarn.setText(position['unRealizedProfit'] + "(" + str(pnl) + "%)")
                    self.labelShortPos.setText(position['entryPrice'])
                    self.labelShortVolume.setText(str(float(position['positionAmt']) * price))
                    try:
                        if pnl >= 1.0:
                            print('shortClose PNL up')
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / SHORT / earn / " + position['unRealizedProfit'])
                            Short = False
                            shortClose()

                        if pnl <= -1.0:
                            print('shortClose PNL down')
                            self.tb1.append(now.strftime('%Y-%m-%d %H:%M:%S') + " / SHORT / loss / " + position['unRealizedProfit'])
                            self.labelShortTime.setText('')
                            self.labelShortPos.setText('')
                            self.labelShortVolume.setText('')
                            self.labelShortEarn.setText('')
                            Short = False
                            switcher = True
                            shortClose()
                    except:
                        pass

                self.labelWallet.setText(str(getBalance()))
                print('long = ' , Long)
                print('short = ', Short)
                sleep(1)
        t1 = Thread(target=runAuto, args=())
        t1.start()


def getBalance():
    account_details = client.futures_account()  # 잔고 표시
    return float(account_details['assets'][8]['marginBalance'])

def getPrice():
    price = float(json.loads(json.dumps(client.futures_ticker(symbol="BTCUSDT"))).get("lastPrice"))
    return price

def getPNL(isLong):
    entryPrice = float(position['entryPrice'])
    try:
        if isLong:
            pnl = (price - entryPrice) / entryPrice * 100 * reverage
            print(pnl)
            return pnl
        elif not isLong:
            pnl = (entryPrice - price) / entryPrice * 100 * reverage
            print(pnl)
            return pnl
    except ZeroDivisionError:
        return 0.0

def getPositionInfo():
    try:
        positions = client.futures_position_information()  # 포지션 정보 가져오기
        symbol = 'BTCUSDT'
        positions = [position for position in positions if position['symbol'] == symbol]

        for position in positions:
            return position
    except:
        return {'symbol': 'BTCUSDT', 'positionAmt': '0', 'entryPrice': '0', 'markPrice': '0', 'unRealizedProfit': '0', 'liquidationPrice': '0', 'leverage': '1', 'maxNotionalValue': '0', 'marginType': 'isolated', 'isolatedMargin': '0', 'isAutoAddMargin': 'false', 'positionSide': 'BOTH', 'notional': '30.06630000', 'isolatedWallet': '30.10075526', 'updateTime': 1687456972244}

def longClose():
    print('long close...')
    order = client.futures_create_order(
        symbol='BTCUSDT',
        side=SIDE_SELL,
        quantity=float(position['positionAmt']),
        closePosition=True,
        reduceOnly=True,
    )
    print('longClose ' , 'quantity = ' , float(position['positionAmt']), ' order = ', order)
    sleep(1)

def shortClose():
    print('short close...')
    order = client.futures_create_order(
        symbol='BTCUSDT',
        side=SIDE_BUY,
        quantity=float(position['positionAmt']),
        closePosition=True,
        reduceOnly=True,
    )
    print('shortClose ', 'quantity = ', float(position['positionAmt']), ' order = ', order)
    sleep(1)

def longOrder():
    order = client.futures_create_order(
        symbol='BTCUSDT',
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=round(wallet * 0.1 / price, 3),
    )
    print('longOrder ', 'quantity = ', round(wallet * 0.1 / price, 3), ' order = ', order)
    sleep(1)

def shortOrder():
    order = client.futures_create_order(
        symbol='BTCUSDT',
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=round(wallet * 0.1 / price, 3),
    )
    print('shortOrder ', 'quantity = ', round(wallet * 0.1 / price, 3), ' order = ', order)
    sleep(1)

def getMyInfo():
    account_info = client.futures_account()
    print(account_info)



if __name__ == '__main__':
    api_key = 'your api key here'
    api_secret = 'yout secret api key here'
    wallet = 10000000
    longPos = 0.0
    shortPos = 0.0
    shortVolume = 0
    longVolume = 0
    longTime = 0
    shortTime = 0
    reverage = 100
    Long = False
    Short = False
    app = QApplication(sys.argv)
    client = Client(api_key, api_secret)

    ex = MyApp()
    sys.exit(app.exec_())



