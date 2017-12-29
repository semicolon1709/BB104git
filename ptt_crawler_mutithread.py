import requests as r
from bs4 import BeautifulSoup as bs
from queue import Queue
from threading import Thread
from datetime import datetime
import json

domain = "http://www.ptt.cc"
first_url = "https://www.ptt.cc/bbs/nba/index.html"
base_url = "https://www.ptt.cc/bbs/nba/index{}.html"



def worker():
    while not queue.empty():
        page = queue.get()
        crawler(page)

def crawler(page):

    '''
    :param page:int 要爬取的page: 
    '''

    print("page " + str(page) + " crawler started")
    url = base_url.format(page)
    page_res = r.get(url)
    soup = bs(page_res.text, "lxml")
    articles = soup.select("div.r-ent")
    for article in articles:
        article_dict = {
            "title": "",
            "category": "",
            "pushCount": "",
            "date": "",
            "author": "",
            "content": ""
        }

        try:
            article_dict['pushCount'] = article.select_one("span.hl").text.strip()
            content_url = article.select_one("div.title > a")["href"].strip()
            soup_content = bs(r.get(domain + content_url).text, "lxml")
            article_dict['author']   = soup_content.select("div.article-metaline")[0]\
                                      .select_one("span.article-meta-value").text.split("(")[0].strip()
            article_dict['title']    = soup_content.select("div.article-metaline")[1]\
                                      .select_one("span.article-meta-value").text.strip()
            article_dict['category'] = soup_content.select("div.article-metaline")[1]\
                                      .select_one("span.article-meta-value").text\
                                      .split(']')[0].split('[')[1].strip()
            article_dict['date']     = soup_content.select("div.article-metaline")[2]\
                                      .select_one("span.article-meta-value").text.strip()
            article_dict['content']  = soup_content.select_one("div#main-content").text
            res_list.append(article_dict)

        except:
            pass
    print("page " + str(page) + " crawler done")


if __name__ == "__main__":
    res_list = []
    threads = []
    queue = Queue()

    res = r.get(first_url)
    soup = bs(res.text, "lxml")
    page_num = int(soup.select_one("div.btn-group-paging").select("a.btn")[1]["href"]\
                  .split("index")[1].split(".")[0]) + 1
    num_thread = 20
    page_grab_num = 2000

    for i in range(page_num, page_num - page_grab_num, -1):  # 將要爬取的頁數放在queue等待
        queue.put(i)
    # 也可改搭配lambda, map, list comprehension 使用
    # list(map(lambda i: queue.put(i), [i for i in range(page_num, page_num - page_grab_num, -1)]))
    
    for j in range(num_thread):  # 建立多執緒清單(執行緒數量:num_thread = 10)
        threads.append(Thread(target=worker))
        # threads = list(map(lambda i:Thread(target=worker), range(num_thread)))
    th_start = datetime.now()
    for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
        threads[i].start()
    for i in range(len(threads)):  # 等所有worker()工作完畢，再執行下一行程式碼:th_end = datetime.now()
        threads[i].join()
    th_end = datetime.now()
    time_spent = str(th_end - th_start).split('.')[0]

    with open('pttCrawler.json', 'w', encoding="utf-8") as f:  # 將res_list存為json檔
        f.write(json.dumps(res_list, ensure_ascii=False, indent=4))

    print("執行緒:" + str(num_thread))
    print("文章數:" + str(len(res_list)))
    print("耗時:" + time_spent)