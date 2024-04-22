# # 匯入模組
# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
# from ibapi.contract import Contract
# import pandas as pd

# class TestApp(EWrapper, EClient):
#     def __init__(self):
#         EClient.__init__(self, self)
#     def historicalData(self, reqId, bar):
#         print("HistoricalData. ReqId:", reqId, "Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.average)

# ib = TestApp()
# ib.connect("127.0.0.1", 7497, clientId=123)

# contract = Contract()
# contract.symbol = "AAPL"
# contract.secType = "STK"
# contract.exchange = "SMART"
# contract.currency = "USD"

# ib.reqHistoricalData(1, contract, "", "1 D", "1 hour", "MIDPOINT", 1, 1, False, [])
# print(ib.reqHistoricalData)
# ib.run()


##

# # 匯入模組
# #from ib_insync import *
# #util.startLoop() # 開啟 Socket 線程
# #ib = IB()
# #ib.connect('127.0.0.1', 7497, clientId=123)
# # 先取得帳戶總覽，'DU228378'是我的 demo 帳號代碼，記得要改成你的 demo 帳號代碼，在 TWS 的右上方尋找
# #account_summary = ib.accountSummary(account='U11510189')
# # 再透過 pandas 轉換為 DataFrame
# #account_summary_df = pd.DataFrame(account_summary).set_index('tag')#取得 Cash 現金的數字
# #account_summary_df.loc['AvailableFunds']#取得 Securities Gross Position Value 持有中資產的帳面價值
# #account_summary_df.loc['GrossPositionValue']#取得 Net Liquidation Value 帳戶清算的總價值
# #account_summary_df.loc['NetLiquidation']
# #print(account_summary_df.loc['NetLiquidation'])


##
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
        def __init__(self):
                EClient.__init__(self, self)
                self.data = [] #Initialize variable to store candle

        def historicalData(self, reqId, bar):
                print(f'Time: {bar.date} Close: {bar.close}')
                self.data.append([bar.date, bar.open,bar.high,bar.low,bar.close])

def run_loop():
        app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
contract = Contract()
contract.symbol = "CL"
contract.secType = "FUT"
contract.exchange = "NYMEX"
contract.currency = "USD"
contract.lastTradeDateOrContractMonth = "202310"


#Request historical candles
app.reqHistoricalData(1, contract, '', '10 D', '30 mins', 'TRADES', 1, 2, False, [])

time.sleep(10) #sleep to allow enough time for data to be returned

#Working with Pandas DataFrames
import pandas

df = pandas.DataFrame(app.data, columns=['DateTime', 'Open','High','Low','Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s')
df.to_csv('CL-30min.csv')

print(df)


app.disconnect()
