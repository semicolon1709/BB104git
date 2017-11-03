import requests as r
import json
from bs4 import BeautifulSoup as bs

def newsURLCrawler(pages=2):
    '''
    爬取蘋果即時新聞連結網址。
    :param pages: 欲爬取的頁數，預設為2頁
    :return: 將產生的新聞連結網址清單傳給contendCrawler()爬取新聞內容
    '''
    linkList = []
    rawURL = "https://tw.appledaily.com/new/realtime/{}"  # 蘋果即時新聞網頁
    soupList = [bs(r.get(rawURL.format(i)).text, "lxml")  for i in range(1,pages+1)] # 產生蘋果新聞頁面的BeautifulSoup文檔

    for soup in soupList: # 逐頁產生該頁的網址清單
        tmpLinkList = list(map(lambda i: soup.select("li.rtddt > a")[i].get("href"), [i for i in range(len(soup.select("li.rtddt > a")))]))
        linkList.extend(tmpLinkList)
    contendCrawler(linkList)

def contendCrawler(linkList):
    '''
    爬蟲新聞內容後，以json格式存檔
    :param linkList: 新聞連結網址清單。
    :return: 以json格式存檔
    '''

    count = 0
    resDict = {}
    with open('/home/yunhan/Desktop/apple.json', 'w') as f:  # 將resDict存為json檔
        for link in linkList:
            articleSoup = bs(r.get(link).text, "lxml")
            titleStr = articleSoup.select_one("hgroup > h1").text.strip()  #爬取新聞標題，做為resDict的key
            timeStr = articleSoup.select_one("hgroup > div.ndArticle_creat").text.split("：")[1].strip()   #爬取新聞時間
            try:
                hotCountStr = articleSoup.select_one("hgroup > div.ndArticle_view").text   #爬取新聞觀看數
            except:#新聞內容不一定有觀看數，使用try except處理
                hotCountStr = "-"
            contentStr = articleSoup.select_one("div.ndArticle_margin > p").text.strip()   #爬取新聞報導內文
            resDict[titleStr] = [timeStr, "viewedCounts:" + hotCountStr, contentStr]   #時間、觀看數及新聞報導內文做為resDict的value
            count += 1
            f.write(json.dumps(resDict, ensure_ascii=False, indent=4))
            print(str(count) + " news grabbed")
    print("All done, news grabbed: " + str(count))

if __name__ == "__main__":
    newsURLCrawler()  # 程式設定每10分鐘爬取1次新聞內容