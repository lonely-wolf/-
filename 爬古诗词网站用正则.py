import requests
from bs4 import BeautifulSoup as bs
import re
import time
import random
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}

content_find = re.compile(r"<.*?>")
dirty = re.compile(r"[，。？!]")
respond = requests.get("https://www.gushiwen.cn/",headers=headers)
respond.encoding = "utf-8"
soup = bs(respond.text,"html.parser")
div = soup.find_all("div",class_="cont")
for all_div in div:
    a = all_div.find("a")
    time.sleep(random.randrange(1,2))
    if a:
        try:
            href = a.get("href")
            all_href = "https://www.gushiwen.cn" + href
            responds = requests.get(all_href,headers=headers)
            responds.encoding = "utf-8"
            soups = bs(responds.text,"html.parser")
            div__ = soups.find_all("div",class_="cont")
            if div__:
                for all_div__ in div__:
                    content = all_div__.find_all("div",class_="contson")
                    if content:
                        title_dirty = all_div__.find("h1")
                        if title_dirty and not re.search(dirty,str(title_dirty.get_text(strip=True))):
                            title_clear = title_dirty.get_text(strip=True)
                            with open(r"C:\Users\admin\Desktop\python\三天计划\三天计划爬虫数据\用re库和bs库一起爬的古诗数据.txt","a",encoding="utf-8")as f:
                                f.write(title_clear+"\n")
                                for i in content:
                                    content_clear = content_find.sub("",i.text)
                                    f.write(content_clear)
                                    f.write("\n")
                                    f.write("-"*30+"\n")
        except:
            print("获取失败")


