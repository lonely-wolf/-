from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import requests
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
    "Referer": "https://www.bilibili.com/"
}
    
driver = webdriver.Edge()
videos = driver.get("https://www.bilibili.com/video/BV1wW1hBME6h/?spm_id_from=333.337.search-card.all.click&vd_source=a4152f22abb1a390d420a08ea2acef79")
time.sleep(5)
# play_buttom = driver.find_element(By.CLASS_NAME,"bpx-player-ctrl-play")
# play_buttom.click()
playinfo = driver.execute_script("return window.__playinfo__")
dash = playinfo["data"]["dash"]
video = dash["video"]
audio = dash["audio"]
best_video = video[0]
best_audio = audio[0]
audio_url = best_audio["baseUrl"]
video_url = best_video["baseUrl"]
a = requests.get(video_url,headers=headers)
b = requests.get(audio_url,headers=headers)
# with open(r"E:\python\爬虫数据\b站视频2.mp4","wb")as f:
#     f.write(a.content)
b = requests.get(audio_url, headers=headers)
print("音频内容长度：", len(b.content))  # 看这里
with open(r"E:\python\爬虫数据\b站音频3.aac","wb")as f:
    f.write(b.content)
