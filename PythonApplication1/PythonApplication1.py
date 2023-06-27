import requests
import json
import cx_Oracle
import time
import sys
from timer import Timer

#print('Start==================================\n\nPython 路径为：', sys.path, '\n')
print("\n启动...")
t0 = Timer()
url = "https://api.gugudata.com/stock/cn?appkey=JMCS6W32BRQL&symbol=300001,300002,300003,300004,300005&begindate=20230601&enddate=20230619&adjust=pre"
payload = {}
headers = {}
t0.start('网络查询')
response = requests.request("GET", url, headers=headers, data=payload)
t0.stop()

en_json = json.loads(response.text)
DataStatus = en_json['DataStatus']
Data = en_json['Data']

k = DataStatus['DataTotalCount']


print('\t返回Data数据共计:', k, ' 行')

# db_conn = cx_Oracle.connect('C##QUANT/a@127.0.0.1:1521/orcl')
db_conn = cx_Oracle.connect('HG/a@127.0.0.1:1521/orcl')
db_cursor = db_conn.cursor()


sql_cmd = 'SELECT  生成查询ID.nextval from dual'
db_cursor.execute(sql_cmd)

for row in db_cursor:
    id = row[0]
print('\t生成的查询ID:', id)

c = [id] + \
    [DataStatus['RequestParameter']] + \
    [DataStatus['StatusCode']] + \
    [DataStatus['StatusDescription']] + \
    [DataStatus['ResponseDateTime']] + [k]

sql_cmd = 'insert into 日交易 values(:1,:2,:3,:4,to_date(:5,\'YYYY-MM-DD HH24:MI:SS\'),:6)'
#print('    插入交易查询表......')
db_cursor.execute(sql_cmd, c)

sql_cmd = 'insert into  日交易记录  values(to_date(:1,\'YYYYMMDD HH24:MI:SS\'),:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)'
i = 0
dataLists = []
while i < k:
    dataList = [str(Data[i]["TimeKey"])+' 23:59:59'] +     \
        [str(Data[i]["Symbol"])] +                  \
        [Data[i]["StockName"]] +                     \
        [Data[i]['Open']] +                         \
        [Data[i]['Close']] +                        \
        [Data[i]['High']] +                         \
        [Data[i]['Low']] +                          \
        [Data[i]['TradingVolume']] +                \
        [Data[i]['TradingAmount']] +                \
        [Data[i]['Swing']] +                        \
        [Data[i]['ChangePercent']] +                \
        [Data[i]['ChangeAmount']] +                 \
        [Data[i]['TurnoverRate']] + [id]
    i = i+1
    dataLists += [dataList]

t0.start('插入oracle')

db_cursor.executemany(sql_cmd, dataLists)
t0.stop()
db_cursor.close()

t0.start('提交')
db_conn.commit()
t0.stop()
db_conn.close()
