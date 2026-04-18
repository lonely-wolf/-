from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
def get_headers():
    headers = input("请输入UA头(可选，不填就直接回车):")
    if headers.strip() == "":
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
            "referer":"https://www.bilibili.com/",
            "Accept-Encoding": "identity",
        }
    else :
        headers = {
            "User-Agent":headers,
            "referer":"https://www.bilibili.com/",
            "Accept-Encoding": "identity",
        }
    return headers

def data():
    url = input("请输入url地址(必须详细网页):")
    place = input("请输入绝对路径:")
    return url,place

def driver_get(url):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(2)
    all = driver.execute_script("return window.__playinfo__")
    # try:
    #     title = driver.find_element(By.CLASS_NAME,"video-title")
    # except:
    #     print("标题获取失败")
    driver.quit()
    return all

def AUDIOandVIDEO_get(all):
    data = all["data"]["dash"]
    audio = data["audio"][0]
    audio_url = audio["baseUrl"]
    video = data["video"][0]
    video_url = video["baseUrl"]
    print(f"解析出音频链接：{audio_url}")
    print(f"解析出视频链接：{video_url}")
    return audio_url,video_url

def main():
    try:
        headers = get_headers()
        url,place = data()
        all = driver_get(url)
        audio_url,video_url = AUDIOandVIDEO_get(all)
        real_audio = requests.get(audio_url,headers = headers)
        real_video = requests.get(video_url,headers = headers)
        with open(fr"{place}/视频.mp4","wb")as f:
            f.write(real_video.content)
        with open(fr"{place}/音频.aac","wb")as f:
            f.write(real_audio.content)
        print("下载成功")
    except:
        print("失败")
main()

# C:\Users\admin\Desktop