import requests as r
from bs4 import BeautifulSoup as bs


def ipGet():
    req = r.get("https://free-proxy-list.net/")
    resList = bs(req.text, "lxml").select_one(".table-striped").select("tbody tr")
    ipList = [resList[i].select("td")[0].text + ":" + resList[i].select("td")[1].text
              for i in range(len(resList))]
    return ipList