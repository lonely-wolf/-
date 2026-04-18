import requests
from bs4 import BeautifulSoup
import time
import random
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Referer": "https://m.zhaobiquge.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=9,image/avif,image/webp,*/*;q=8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
encoding="utf-8"
for n in range(1,49):
    respond = requests.get(f"https://m.zhaobiquge.com/biquge/34/34104/index_{n}.html",headers=headers)
    soup = BeautifulSoup(respond.text,"html.parser")
    situations = soup.find_all("ul",class_="chapter")
    situation = situations[0]
    li = situation.find_all("li")
    with open(r"E:\python\爬虫数据\蛊真人1.txt","a",encoding="utf-8")as f:
        if li:
            for i in li:
                a=i.find("a")
                things=a.get("href")
                full_things="https://m.zhaobiquge.com/"+things
                print(full_things)
                try:
                    in_respond = requests.get(full_things,headers=headers)    
                    final_soup = BeautifulSoup(in_respond.text,"html.parser")
                    div = final_soup.find("div",class_="reader-main")
                    h1_title = final_soup.find("div",class_="nr_title")
                    title = h1_title.get_text(strip=True)
                    word_read = final_soup.find("div", class_="nr_nr")
                    f.write(title)
                    f.write("\n"*2)
                    if word_read:
                        para = word_read.find_all("p")
                        for j in para:
                            f.write(j.text)
                            f.write("\n") 
                            f.flush()
                    print("\n"*8)
                    time.sleep(random.randint(0,3))
                except Exception as e:
                    print("失败原因：", e)