import requests as r
from bs4 import BeautifulSoup as bs
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import json

domain = "http://www.ptt.cc"
firstURL = "https://www.ptt.cc/bbs/nba/index.html"
baseUrl = "https://www.ptt.cc/bbs/nba/index{}.html"
resList = []
queue = Queue()

def crawler(page):
    
    '''
    :param page:int 要爬取的page: 
    '''
    
    url =baseUrl.format(page)
    res = r.get(url)
    soup = bs(res.text, "lxml")
    articleNum = soup.select("div.r-ent")
    for article in range(len(articleNum)):
        articleDict = {
            "title": "",
            "category": "",
            "pushCount": "",
            "date": "",
            "author": "",
            "content": ""
        }

        try:
            articleDict['pushCount'] = articleNum[article].select_one("span.hl").text.strip()
            contentUrl = articleNum[article].select_one("div.title > a")["href"].strip()
            soupContent = bs(r.get(domain + contentUrl).text, "lxml")
            articleDict['author']   = soupContent.select("div.article-metaline")[0]\
                                      .select_one("span.article-meta-value").text.split("(")[0].strip()
            articleDict['title']    = soupContent.select("div.article-metaline")[1]\
                                      .select_one("span.article-meta-value").text.strip()
            articleDict['category'] = soupContent.select("div.article-metaline")[1]\
                                      .select_one("span.article-meta-value").text\
                                      .split(']')[0].split('[')[1].strip()
            articleDict['date']     = soupContent.select("div.article-metaline")[2]\
                                      .select_one("span.article-meta-value").text.strip()
            articleDict['content']  = soupContent.select_one("div#main-content").text
            resList.append(articleDict)
        except:
            pass
    print("page:" + str(page) + " done")

if __name__ == "__main__":

    numThread = 10
    page_grab_num = 18


    res = r.get(firstURL)
    soup = bs(res.text, "lxml")
    pageNum = int(soup.select_one("div.btn-group-paging").select("a.btn")[1]["href"]\
                  .split("index")[1].split(".")[0]) + 1

    # threads = ThreadPoolExecutor(numThread)
    # futures = []
    # thStart = datetime.now()
    # for page in range(pageNum, pageNum - page_grab_num, -1):
    #     futures.append(threads.submit(crawler, page))
    # wait(futures)
    # thEnd = datetime.now()
    # timeSpent = str(thEnd - thStart).split('.')[0]
    #
    # with open('pttCrawler.json', 'w', encoding="utf-8") as f:  # 將resList存為json檔
    #     f.write(json.dumps(resList, ensure_ascii=False, indent=4))
    #
    # print("執行緒:" + str(numThread))
    # print("文章數:" + str(len(resList)))
    # print("耗時:" + timeSpent)

    pageList = [ page for page in range(pageNum, pageNum - page_grab_num, -1)]
    thStart = datetime.now()
    with ThreadPoolExecutor(max_workers=numThread) as executor:
        for page, data in zip(pageList, executor.map(crawler, pageList)):
            print('page:{} done'.format(page))
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]

    print("執行緒:" + str(numThread))
    print("文章數:"+ str(len(resList)))
    print("耗時:" + timeSpent)


