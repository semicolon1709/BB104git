import requests as r
import json
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from datetime import timedelta as tdel



def newsURLCrawler(pages=1, minutes=20):
    '''
    爬取蘋果即時新聞連結網址。
    :param pages: int 欲巡查的新聞頁數，預設為1頁
    :param minutes: int 爬取離現在時間幾分鐘內的新聞內容，預設為20分鐘
    :return: 將產生的新聞連結網址清單、幾分鐘內新聞的參數，傳給contendCrawler()爬取新聞內容
    '''
    linkList = []
    rawURL = "https://tw.appledaily.com/new/realtime/{}"  # 蘋果即時新聞網頁
    soupList = [bs(r.get(rawURL.format(i)).text, "lxml")  for i in range(1,pages+1)] # 產生蘋果新聞頁面的BeautifulSoup文檔
    intervalTime = minutes
    for soup in soupList: # 逐頁產生該頁的網址清單
        tmpLinkList = list(map(lambda i: soup.select("li.rtddt > a")[i].get("href"), [i for i in range(len(soup.select("li.rtddt > a")))]))
        linkList.extend(tmpLinkList)
    contendCrawler(linkList, intervalTime)

def contendCrawler(linkList, intervalTime):
    '''
    爬蟲新聞內容後，以json格式存檔
    :param linkList: List 新聞連結網址清單。
    :param intervalTime: int 爬取離現在時間幾分鐘內的新聞內容
    :return: 以json格式存檔
    '''

    count = 0
    resDict = {}
    timeList = intervalTimeListGenerator(intervalTime) # 產生時間清單
    with open('./apple.json', 'w') as f:  # 將resDict存為json檔
        for link in linkList:
            articleSoup = bs(r.get(link).text, "lxml")
            timeStr = articleSoup.select_one("hgroup > div.ndArticle_creat").text.split("：")[1].strip()  # 爬取新聞時間
            if timeStr.split(" ")[1] in timeList:
                titleStr = articleSoup.select_one("hgroup > h1").text.strip()  #爬取新聞標題，做為resDict的key
                try:
                    hotCountStr = articleSoup.select_one("hgroup > div.ndArticle_view").text   #爬取新聞觀看數
                except:  #新聞內容不一定有觀看數，使用try except處理
                    hotCountStr = "-"
                contentStr = articleSoup.select_one("div.ndArticle_margin > p").text.strip()   #爬取新聞報導內文
                resDict[titleStr] = [timeStr, "viewedCounts:" + hotCountStr, contentStr]   #時間、觀看數及新聞報導內文做為resDict的value
                count += 1
                f.write(json.dumps(resDict, ensure_ascii=False, indent=4))
                print(str(count) + " news grabbed")
            else:
                break
    print("All done, news grabbed: " + str(count))

def intervalTimeListGenerator(minutes):
    '''
    依傳入的時間，產生時間List
    :param minutes: int  離現在時間幾分鐘內的數字
    :return: List
    '''
    timeList = [(dt.now()+tdel(minutes=-i)).strftime("%H:%M") for i in range(minutes)]
    return timeList

if __name__ == "__main__":
    newsURLCrawler()  # 系統排程設定，每20分鐘執行程式爬取1次最新新聞內容
