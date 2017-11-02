import requests as r
from bs4 import BeautifulSoup as bs
import re

# 給header讓amazon認為我們不是機器人，而是透過Chrome索取資料
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
}
count = 0
urlList = []
quryUrl = "https://www.amazon.com/s/?page={}&keywords=surfboard"
for i in range(3):   # 爬取3頁的商品頁面
    res = r.get(quryUrl.format(i), headers=headers)
    soup = bs(res.text, "lxml")

    for j in range(len(soup.select('a.s-access-detail-page'))):   # 每單頁面裡的商品網址連結
        rawItemUrl = soup.select('a.s-access-detail-page')[j].get('href')
        if rawItemUrl.startswith('https'):    #只有開頭是https  才是我們要的連結
            urlList = re.findall('(https://www.amazon.com/.+/dp/.+)/ref=', rawItemUrl)  # 精簡網址長度
                                                                                        # 注意：返回值資料型態為LIST
            count += 1
            print(count)
            print(urlList)
            with open('./{}.html'.format(urlList[0].split('/')[-1]), 'w') as f:
                f.write(r.get(urlList[0], headers=headers).text)    # 由商品網址中，下載商品內頁內容存檔
