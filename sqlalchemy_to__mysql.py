import requests as r
import sqlalchemy
import pandas

res = r.get("https://free-proxy-list.net/")
data = pandas.DataFrame(pandas.read_html(res.text)[0])
data = data.loc[:, ["IP Address", "Port"]]
data = data.drop(data.index[[len(data)-1]])
data["Port"] = data["Port"].astype(int).astype(str)  # 1.pandas讀入為float，Host有小數點，轉成int
                                                     # 2.mysql不支援numpy float64，轉成字串
data["IP"] = data["IP Address"] + ":" + data["Port"]
data = data.loc[:, ["IP"]]
print(data)
# engine = sqlalchemy.create_engine("mysql+pymysql://root:iii@127.0.0.1:3305/?charset=utf8mb4")   建立資料庫
# engine.execute("CREATE DATABASE IP_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")     採用utf-8編碼
engine = sqlalchemy.create_engine("mysql+pymysql://root:iii@127.0.0.1:3305/IP_data?charset=utf8mb4")
				#('mysql+pymysql://accout:passward@127.0.0.1:3306/(database_name)?charset=utf8mb4')
                                # 預設是mysqldb，改成pymysql
data.to_sql('IP_table', engine, if_exists='append', index=False)




