import requests as req
import re
from bs4 import BeautifulSoup as bs
import time as ti

def link(url):
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "cookie" : "uuid_n_v=v1; uuid=9C3F46509FDE11EAB27719E1F7042D98A186551371544325A41B023BAFEE3BCF; _csrf=f73687f23f4bd9389afee769913ab9251ef6b2d8bd48c4334d518307e414539b; mojo-uuid=d3b23fa239af91a459c4b2f6c9de719c; _lxsdk_cuid=17254b2e1a9c8-052eae284a85d8-f7d1d38-1fa400-17254b2e1a9c8; _lxsdk=9C3F46509FDE11EAB27719E1F7042D98A186551371544325A41B023BAFEE3BCF; mojo-session-id={'id':'2ac8505efd1ae69f992579cb636fb214','time':1590558909003}; lt=BpbAI8HcP4rjxW8EMW-plp3nTJUAAAAArwoAAFrS_NePLpJnd8RvQOFnAcC1hTuWOB-rjKsdTPcXXBPgmrPLi7_lS4h6J6aBdQckBw; lt.sig=XlSVzQd8TszxuaUX6ZGwidXDiRc; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1590558909,1590560706,1590560728; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1590560728; __mta=216439465.1590558909112.1590560705986.1590560727890.4; mojo-trace-id=7; _lxsdk_s=17254b2e1aa-3cf-053-a27%7C%7C9"
    }
    res = req.get(url,headers = header)
    if res.status_code == 200:
        return bs(res.text,"lxml")
    return None

for i in range(0,100,10):
    url = "https://maoyan.com/board/4?offset=" + str(i)
    movies = link(url).find_all("dd")
    for i in movies:
        img = i.find("img",class_ = "board-img").get("data-src")
        num = i.find("i").text
        name = i.find("a").get("title")
        actor = re.findall("主演：(.*)",i.find("p",class_ = "star").text)[0]
        when = re.findall("上映时间：(.*)",i.find("p",class_ = "releasetime").text)[0]
        score = i.find("i",class_ = "integer").text + i.find("i",class_ = "fraction").text
        url1 = "https://maoyan.com" + i.find("p",class_ = "name").a.get("href")
        movie = link(url1)
        ti.sleep(1)
        about = movie.find("span",class_ = "dra").text
        word = movie.find("span",class_ = "name").text +  ":  " + movie.find("div",class_ = "comment-content").text.replace("😫","")
        boss = movie.find("a",class_= "name").text.replace("\n","").replace(" ","")

        a = {
            "片名" : name,
            "排名" : num,
            "评分" : score,
            "网址" : url1,
            "演员" : actor,
            "上映时间" : when,
            "图片" : img,
            "评论" : word,
            "导演" : boss,
            "简介" : about
        }
