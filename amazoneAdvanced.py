import requests as r
from bs4 import BeautifulSoup as bs


def amazon_crawler(item_name, pages):

    '''
    :param item_name:想爬取的商品名稱
    :param pages: 想爬取的頁數
    :return: 於當前的資料夾儲存商品網頁---(商品編號.html)
    '''

    pageCount = 0
    urlList = []
    quryUrl = "https://www.amazon.com/s/?page={}&keywords={}"
    contentCount = 0

    # 給header讓amazon認為我們不是機器人，而是透過Chrome索取資料
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
    }

    soupList = [bs(r.get(quryUrl.format(pages, item_name), headers=headers).text,"lxml") for i in range(pages)] # 產生每一頁的BeautifulSoup文檔

    # 爬取每一頁的商品連結網址
    for soup in soupList:
        urlNumList = [i for i in range(len(soup.select('a.s-access-detail-page')))] # 該頁共有i個商品連結,即len(urlNumList)=i
        rawUrlList = list(map(lambda i: soup.select('a.s-access-detail-page')[i].get("href"), urlNumList)) # 產生該頁的商品連結
        urlList.extend(rawUrlList)
        pageCount += 1
        print("page{}:grabbed, {}urls".format(pageCount, len(rawUrlList)))

    for url in urlList:
        if url.startswith("https"):
            with open('./{}.html'.format(url.split('/ref')[0]).split("dp/")[1], 'w') as f:
                f.write(r.get(url, headers=headers).text)    # 由商品網址中，下載商品內頁內容存檔
                contentCount += 1
                print("itemHTML grabbed:" + str(contentCount))

if __name__ == "__main__":
    amazon_crawler("surf", 2)
    print("done")