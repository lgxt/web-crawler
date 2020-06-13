from selenium import webdriver
import requests
import json
import os
import re
import random
import time
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd
import os
from pathlib import Path
from goto import with_goto


def automatics(query_list,sleeps):
    # 设置路径
    work_dir = Path.cwd().parent / 'csv'
    if not work_dir.exists():
        work_dir.mkdir()

    # 调用谷歌浏览器驱动   如果本地电脑未安装谷歌驱动，请网上下载
    # 请将 chromedriver 移动至根目录
    driver = webdriver.Chrome()
    # 微信公众平台网址
    driver.get("https://mp.weixin.qq.com/")
    time.sleep(10) # 在这个时候要点击一下使用账号登陆否则报错
    driver.find_element_by_name("account").clear()
    # 微信公众号
    driver.find_element_by_name("account").send_keys("likeyu1014@163.com")
    driver.find_element_by_name("password").clear()
    time.sleep(2)
    # 微信公众号密码
    driver.find_element_by_name("password").send_keys("lky1014163")
    driver.find_element_by_class_name("icon_checkbox").click()
    time.sleep(2)
    driver.find_element_by_class_name("btn_login").click()
    time.sleep(120)

    ##获取cookie
    driver.get('https://mp.weixin.qq.com/')
    cookies = driver.get_cookies()
    cookie = {}
    for items in cookies:
        cookie[items.get('name')] = items.get('value')
    with open('cookies.txt','w') as file:
        file.write(json.dumps(cookie))
    driver.close()
    with open('cookies.txt','r') as file1:
        cookie = file1.read()
    cookies = json.loads(cookie)
    os.remove('cookies.txt')
    for query in query_list:
        # 从url中获取token
        url = "https://mp.weixin.qq.com"
        response = requests.get(url, cookies=cookies)
        token = re.findall(r'token=(\d+)', str(response.url))[0] # 有时会随机报错，重试就好，可能你扫码的速度慢

        #随机user-agent
        user_agent_list=[]
        for i in range(30):
            ua = UserAgent()
            user_agent_list.append(ua.chrome)
        UserAgents = random.choice(user_agent_list)

        header = {
                "HOST": "mp.weixin.qq.com",
                "User-Agent": UserAgents
                 }

        #搜索公众号的接口地址
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        query_id = {
            'action': 'search_biz',
            'token' : token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query, # 公众号名字
            'begin': '0',
            'count': '5'
            }
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')

        #微信公众号文章接口地址
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'

        # 设置微信公众号params
        query_id_data = {
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "random": random.random(),
            "action": "list_ex",
            "begin": "0",
            "count": "5",
            "query": "",
            "fakeid": fakeid,
            "type": "9",
            }

        content_list = []
        # 使用代理ip
        proxy_pool_url = 'http://localhost:5555/random'
        proxy = requests.get(proxy_pool_url)
        if response.status_code != 200:
            print("进入微信公众号列表--proxy失败")
        proxy = proxy.text.strip()
        proxies = {'http': 'http://' + proxy}
        try:
            #微信公众号列表
            appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data, proxies=proxies)
            max_num = appmsg_response.json().get('app_msg_cnt') #文章数
            num = int(int(max_num) / 5) #页数
        except:
            print("进入微信公众号列表--请求失败",'query=',query)
        begin= 430
        num= 120
        while num +1> 0 :
            query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
            }
            print('正在翻页：--------------',begin)
            proxy = requests.get(proxy_pool_url)
            if response.status_code != 200:
                print("下载页面失败--proxy错误",'begin=',begin,'num=',num,'query=',query)
            proxy = proxy.text.strip()
            proxies = {'http': 'http://' + proxy}
            try:
                query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
                fakeid_list = query_fakeid_response.json().get('app_msg_list')
                for item in fakeid_list:
                    items = []
                    items.append(item["title"])
                    items.append(item["link"])
                    content_list.append(items)
                num -= 1
                begin = int(begin)
                begin+=5
                time.sleep(random.randint(sleeps,sleeps+60))
            except:
                print("下载页面失败--请求错误", 'begin=', begin, 'num=', num, 'query=', query)
                break
        name= ['title','link']
        test= pd.DataFrame(columns=name,data=content_list)
        test = test.drop_duplicates(['title'])
        test.to_csv(os.path.join(work_dir,"{}.csv".format(query)),mode='a',encoding='utf-8-sig')
automatics(query)
