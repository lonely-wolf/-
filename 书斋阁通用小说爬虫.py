import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random
import logging
from tqdm import tqdm
headers = input("输入你的UA头(可选，不填就直接回车):")
if headers == "":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        "Referer": "https://www.shuzhaige.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=9,image/avif,image/webp,*/*;q=8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
else:
        headers = {
        "User-Agent": f"{headers}",
        "Referer": "https://www.shuzhaige.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=9,image/avif,image/webp,*/*;q=8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

#获取小说标题
url = input("输入URL(仅限书斋阁):")
place = input("输入你的下载绝对路径:")
respond = requests.get(url,headers = headers)
respond.encoding = "utf-8"
soup = bs(respond.text,"html.parser")
title_div = soup.find("div",class_ = "m-infos")
title_h1 = title_div.find("h1")
title = title_h1.get_text(strip=True)

#logging日志初始化
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s",
    encoding="utf-8",
    filename=f"{title}_spider.log",
    filemode="a"
)

#多线程数输出初始化
def threading_():
    while(True):
        for t in threading.enumerate():
            print(t.name)
        time.sleep(5)


#整个小说网页链接获取
def all_url():
    all_list = []
    div = soup.find("div",class_ = "m-book-list")
    ul = div.find("ul")
    li = ul.find_all("li" , class_ = "line3")
    for all in li:
        try:
            a = all.find("a")
            href = a.get("href")
            real_url = href
            all_list.append(real_url)
            time.sleep(random.uniform(0.1,0.3))
            logging.info("链接获取成功！")
        except Exception as e:
            logging.error(f"链接获取失败，详细原因：{e}")
    return all_list

#每一个线程的工作内容
def one_thread_how_work(real_url):
    try:
        respond = requests.get(real_url,headers = headers)
        respond.encoding = "utf-8"
        soup = bs(respond.text,"html.parser")
        logging.info("网页解析成功！")
        div = soup.find("div",class_ = "m-title col-md-12")
        title = div.find("h1").get_text(strip=True)
        content = title
        div= soup.find("div",class_ = "panel-body")
        p = div.find_all("p")
        for all in p:
            content += all.text+"\n"
            logging.info("内容爬取成功！")
            time.sleep(random.uniform(0.001,0.003))
    except Exception as e:
        logging.error(f"内容爬取失败，详细原因:{e}")
    return content

#主函数
if __name__=="__main__":
    #后台监控线程
    monitor_thread = threading.Thread(target=threading_, daemon=True)
    monitor_thread.start()
    #下载主程序
    all_ = all_url()
    total_chapters = len(all_)
    with ThreadPoolExecutor(max_workers=15) as executor:
        all_content = list(tqdm(
            executor.map(one_thread_how_work, all_),
            total=total_chapters,  # 进度条知道总数
            desc="📚 爬取进度",    # 左边文字
            ncols=70,             # 进度条长度
            colour="green"        # 绿色进度条
        ))
    with open(fr"{place}\{title}.txt","w",encoding = "utf-8")as f:
        for i in all_content:
            f.write(i+"\n")

