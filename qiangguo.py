from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import re
import json
import random
from selenium.webdriver.common.keys import Keys
browser=webdriver.Chrome()
calDict = {
            "zhongyaoxinwen": "https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html",
            "zhongyaohuodong": "https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaohuiyi": "https://www.xuexi.cn/89acb6d339cd09d5aaf0c2697b6a3278/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaojianghua": "https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhongyaowenzhang": "https://www.xuexi.cn/6db80fbc0859e5c06b81fd5d6d618749/9a3668c13f6e303932b5e0e100fc248b.html",
            "chuguofangwen": "https://www.xuexi.cn/2e5fc9557e56b14ececee0174deac67f/9a3668c13f6e303932b5e0e100fc248b.html",
            "zhishipishi": "https://www.xuexi.cn/682fd2c2ee5b0fa149e0ff11f8f13cea/9a3668c13f6e303932b5e0e100fc248b.html",
            "handianzhici": "https://www.xuexi.cn/13e9b085b05a257ed25359b0a7b869ff/9a3668c13f6e303932b5e0e100fc248b.html",
            "xinshidaijishi": "https://www.xuexi.cn/9ca612f28c9f86ad87d5daa34c588e00/9a3668c13f6e303932b5e0e100fc248b.html",
            "xuexishipin": "https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html",
            "zonghexinwen": "https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html"
            }

def getVideoList(jsUrl):
        res = requests.get(jsUrl)
        res.encoding= 'utf-8'
        jsondata = json.loads(res.text.lstrip("globalCache = ").rstrip(";"))
        videoList = []
        for key,value in jsondata.items():
            if key == "sysQuery":
                pass
            elif key!= 'sysQuery':
                outsidevalue =  value
                try:
                    for key,value in outsidevalue.items():
                        list = value
                        for unit in list:
                            unitdict = {}
                            unitdict['static_page_url']=unit['static_page_url']
                            unitdict['frst_name']=unit['frst_name']
                            unitdict['cate_id']=unit['cate_id']
                            unitdict['type']=unit['type']
                            try:
                                unitdict['imgUrl'] = json.loads(unit['thumb_image'], encoding="utf-8")[0]['thumbInfo']
                            except:
                                    pass
                            try:
                                unitdict['original_time'] = unit['original_time']
                            except:
                                pass
                            videoList.append(unitdict)
                except:
                    pass
        else:
            return videoList

def getArticle(newsUrl):
    artList=[]
    # print(newsUrl)
    jsUrlTemp = newsUrl.rsplit('/')
    jsUrl = jsUrlTemp[0] + '//' + jsUrlTemp[2] + '/' + jsUrlTemp[3] + '/data' + jsUrlTemp[4].replace('html', 'js')
    res = requests.get(jsUrl)
    res.encoding = 'utf-8'
    for key,value in json.loads(res.text.lstrip('globalCache = ').rstrip(';'),encoding="utf-8").items():
        if key != 'sysQuery':
            for item in  value['list']:
                # print(item['static_page_url'],item['frst_name'])
                artList.append(item['static_page_url'])
    return artList

def requestArticle(lis):
    browser.get(lis[random.randint(0,len(lis)-1)])
    # js="var q=document.documentElement.scrollTop=200"  
    # browser.execute_script(js)
    # time.sleep(5)
    # js="var q=document.documentElement.scrollTop=2000"  
    # browser.execute_script(js)
    # time.sleep(5)
    # js="var q=document.documentElement.scrollTop=5000"  
    # browser.execute_script(js)
    for t in range(10,5000,200):
        js="var q=document.documentElement.scrollTop=" + str(t)
        time.sleep(1)
        browser.execute_script(js)
    # time.sleep(50)

calRats = getArticle(calDict[random.choice(list(calDict))])

browser.get('https://pc.xuexi.cn/points/my-points.html')
js="var q=document.documentElement.scrollTop=10000"  
browser.execute_script(js)
time.sleep(5)

a = input("先看文章（输入：1）还是先看视频（输入：2）：")
if a == '1':
    # 阅读文章
    for i in range(10):
        requestArticle(calRats)
        time.sleep(30)
        print(i) 
    #看视频
    videoList = getVideoList("https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js")
    i = 0
    for item in range(1000):
        if i > 20:
            break
        browser.get(videoList[random.randint(0,len(videoList)-1)]['static_page_url'])
        js="var q=document.documentElement.scrollTop=500"
        browser.execute_script(js)
        print(i)
        try:
            browser.find_element_by_tag_name("video")
            time.sleep(180)
            i += 1
        except Exception:
            time.sleep(10)


else:
    #观看视频
    videoList = getVideoList("https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/datadb086044562a57b441c24f2af1c8e101.js")
    i = 0
    for item in range(1000):
        if i > 10:
            break
        browser.get(videoList[random.randint(0,len(videoList)-1)]['static_page_url'])
        js="var q=document.documentElement.scrollTop=500"
        browser.execute_script(js)
        print(i)
        try:
            browser.find_element_by_tag_name("video")
            time.sleep(180)
            i += 1
        except Exception:
            time.sleep(10)
    # 阅读文章
    for i in range(10):
        requestArticle(calRats)
        time.sleep(30)
        print(i) 


    
