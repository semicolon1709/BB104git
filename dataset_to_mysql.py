import requests as r
import dataset
import pandas

res = r.get("https://free-proxy-list.net/")
data = pandas.DataFrame(pandas.read_html(res.text)[0])
data = data.loc[:, ["IP Address", "Port"]]
data = data.drop(data.index[[len(data)-1]])
data["Port"] = data["Port"].astype(int).astype(str)  # 1.pandas讀入為float，Host有小數點，轉成int
                                                     # 2.mysql不支援numpy float64，轉成字串
data["IP"] = data["IP Address"] + ":" + data["Port"]
db = dataset.connect('mysql+pymysql://root:iii@127.0.0.1:3305/ipdata?charset=utf8mb4')
                   #('mysql+pymysql://accout:passward@127.0.0.1:3306/(database_name)?charset=utf8mb4')
                   # 預設是mysqldb，改成pymysql
table = db['IP_table']
for i in range(len(data)-1):
    table.insert(dict(data.loc[i, ["IP"]])) #table.insert()參數為 dict

#data_to_sql = list(map(lambda x: table.insert(x), [dict(data.loc[i, ["IP"]]) for i in range(len(data)-1)]))
## 搭配 map、lambda、list comprehension使用




