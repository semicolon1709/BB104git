import requests as r
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import json
from getIP import iplist
import random
from pymongo import MongoClient

def crawler(page, ipList):
    '''

    :param page: int, 商品頁碼
    :param ipList: list, ip列表
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
    }

    proxies = {"http": "http://{}".format(ipList[random.randint(0, len(ipList))])} #自ipList隨機取1個ip

    timeout = 10

    count = 1
    while True:
        try:
            if count == 5:
                print("page:" + page + " not found")
                return
            if count == 3:
                proxies = {"http": "http://{}".format(ipList[random.randint(0, len(ipList))])}
            soup = bs(r.get(url.format(page), headers=headers, proxies=proxies, timeout=timeout).text, "lxml")
            break
        except:
            count += 1

    items = soup.select("div.s-item-container")  # 找尋該頁面有多少商品
    for i in range(len(items)):  #逐筆抓取商品資訊
        try:
            productDict = {
                "productName": "",
                "price": "",
            }
            productName = items[i].select_one("h2").text
            if productName not in productNameList:
                productNameList.append(productName)
                tmpURL = items[i].select_one("a.s-access-detail-page")["href"]
                productURL = (tmpURL if tmpURL.startswith("http") else domin + tmpURL)
                count = 1
                while True:
                    try:
                        if count == 5:
                            print("product:" + productURL + " not found")
                            return
                        if count == 3:
                            proxies = {"http": "http://{}".format(ipList[random.randint(0, len(ipList))])}
                        productContent = bs(r.get(productURL, headers=headers, proxies=proxies, timeout=timeout).text, "lxml")
                        break
                    except:
                        count += 1
                productDict["productName"] = productName
                productDict["price"] = productContent.select_one("#priceblock_ourprice").text.strip()
                resList.append(productDict)
                print("product:" + productDict["productName"] + " grabbed")
        except:
            pass


if __name__ == "__main__":

    keyword = input("輸入搜尋商品名稱:")
    pageNum = int(input("欲爬取多少頁:"))
    numThread = int(input("執行緒數量:"))

    domin = "https://www.amazon.de"
    url = "https://www.amazon.de/s/url=search-alias%3Dsports&field-keywords=" + keyword + "&page={}"
    resList = []
    productNameList = []

    print("getting iplist...")
    ipList = iplist()      #獲取ip列表，爬取網路代理伺服器用
    print(ipList)
    print("got iplist")

    threads = ThreadPoolExecutor(numThread)  #設定多執行緒
    futures = [threads.submit(crawler, page, ipList) for page in range(pageNum)]  #將工作事項交給futures管理
    thStart = datetime.now()
    wait(futures)               #啟動執行緒，並等所有工作完成後，再執行下一行程式碼
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]

    with open('amazonCrawler.json', 'w', encoding="utf-8") as f:  # 將resList存為json檔
        f.write(json.dumps(resList, ensure_ascii=False, indent=4))


    print("執行緒:" + str(numThread))
    print("商品數:" + str(len(resList)))
    print("耗時:" + timeSpent)

# client = MongoClient('localhost', 27017)
# db = client['amazonDe']
# db.product.insert_many(resList)
