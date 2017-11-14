import requests as r
from bs4 import BeautifulSoup as bs
import re


data = {
    "categoryId": "1277",
    "orderBy": "21",
    "pageIndex": "1",
    "pageSize": "1000",
    "isLoadThree": "false",
}

domin = "https://online.carrefour.com.tw/"
res = r.post("https://online.carrefour.com.tw/Catalog/CategoryJson", data=data)
hrefList = re.findall('"SeName":"/(\d+)\?categoryId', res.text)    #正規表示法取回商品的id
finalList = []
count = 0
for product in hrefList:  #逐筆request 商品頁面取回所要的資訊
    productDict = {
        "title": "",
        "price": 0,
        "url": ""
    }

    productURL = domin + product
    productRes = r.get(productURL)
    productSoup = bs(productRes.text, "lxml")
    productDict["url"]   = productURL
    productDict["title"] = productSoup.select_one("div.pro-name").text
    productDict["price"] = int(productSoup.select_one("div.pro-price").select_one(".red").text.split("$")[1])
    finalList.append(productDict)
    count += 1
    print(str(count) + " items grabbed")
