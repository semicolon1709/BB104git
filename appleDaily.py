import requests as r
import json
from bs4 import BeautifulSoup as bs



pageContentList = []

rawURL = "https://tw.appledaily.com/new/realtime/{}" #蘋果即時新聞網頁

def newsURLClawer(pages=5):
    '''
    爬取蘋果即時新聞連結網址。
    參數：page-欲爬取的頁數，預設為5頁。
    '''

    linkList = []

    for i in range(1,pages+1):
        res = r.get(rawURL.format(i))
        soup = bs(res.text, "html5lib")
        for i in range(len(soup.select("li.rtddt > a"))):
            urlStr = soup.select("li.rtddt > a")[i].get("href")
            linkList.append(urlStr)
            print(urlStr)
    contendClawer(linkList)



def contendClawer(linkList):
    '''
       依傳入的蘋果即時新聞連結網址爬取新聞內容。
       參數：linkList-新聞網址 LIST。
    '''

    count = 0
    resDict = {}
    for link in linkList:
        article = r.get(link)
        articleSoup = bs(article.text, "html5lib")
        titleStr = articleSoup.select_one("hgroup > h1").text.strip()  #爬取新聞標題，做為resDict的key
        timeStr = articleSoup.select_one("hgroup > div.ndArticle_creat").text.split("：")[1].strip() #爬取新聞時間
        try:
            hotCountStr = articleSoup.select_one("hgroup > div.ndArticle_view").text  #爬取新聞觀看數
        except:#新聞內容不一定有觀看數，使用try except處理
            hotCountStr = "-"
        contentStr = articleSoup.select_one("div.ndArticle_margin > p").text #爬取新聞報導內文
        resDict[titleStr] = [timeStr, "人氣:" + hotCountStr, contentStr]#時間、觀看數及新聞報導內文做為resDict的value
        count+=1
        print(count)
        print(resDict[titleStr])
    with open('/home/yunhan/Desktop/apple.json', 'w') as f:  #將resDict存為json檔
        f.write(json.dumps(resDict, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    newsURLClawer(3)