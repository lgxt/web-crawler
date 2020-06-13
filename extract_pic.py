# -*- coding:utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from fake_useragent import UserAgent
import random
import uuid
import re
import filetype

def extract_pic(query):
    work_dir = Path.cwd().parent
    import_html_dir = work_dir / 'html' / query
    dir = work_dir / 'pic'
    if not dir.exists():
        dir.mkdir()
    pic_dir = work_dir / 'pic' / query
    if not pic_dir.exists():
        pic_dir.mkdir()

    #设置user-agent
    user_agent_list=[]
    for i in range(30):
        ua = UserAgent()
        user_agent_list.append(ua.chrome)
    UserAgents = random.choice(user_agent_list)
    header = {
            "User-Agent": UserAgents
             }

    reg_all = ['data-src="(.+?)"',':image" content="(.+?)"'] #识别图片链接的正则表达
    for file in list(import_html_dir.glob('*.html')):
        filename = os.path.basename(file)
        tar_link = work_dir / 'pic' / query / filename.rstrip('.html')
        if not os.path.exists(tar_link):
            tar_link.mkdir()
            with open(file, encoding='utf-8') as f:
                html_content = f.read()
            imglist = []
            # 获得图片链接列表
            for reg in reg_all:
                imgre = re.compile(reg)
                imglist = re.findall(imgre, html_content)+imglist
            imglist = list(set(imglist)) 
            print(imglist)
            for item in imglist:
                if not item.startswith('http'):
                    item = f'http://{item}'
                try: #图片下载，只下载jpeg与gif类
                    img_data = requests.get(item, headers=header).content
                    if str(filetype.guess(img_data)).count('Jpeg')>0 or str(filetype.guess(img_data)).count('Gif')>0:
                        style=re.split(r'[.\s]',str(filetype.guess(img_data)))[3].lower()
                        with open(os.path.join(tar_link, f'{uuid.uuid4().hex}.{style}'), 'w+') as f:
                            f.buffer.write(img_data)
                except:
                    print('error',filename,item)
            time.sleep(3) #下载图片不需要限速
extract_pic('金蝶')
