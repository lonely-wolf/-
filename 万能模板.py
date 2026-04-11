import requests
from bs4 import BeautifulSoup as bs
import time
import re
import random
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"
}
#这里输入url就行
url = ""
respond = requests.get(url,headers=headers)
respond.encoding = "utf-8"
soup = bs(respond.text,"html.parser")
time.sleep(random.randrange(1,2.5))
#下面就按网页实时不同写就行了
