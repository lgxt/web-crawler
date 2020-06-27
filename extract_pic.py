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
import pandas as pd

def extract_pic(query):
    import_html_dir = Path.cwd().parent / 'html' / query
    dir = Path.cwd().parent / 'pic'
    work_dir = Path.cwd().parent / 'csv'
    if not dir.exists():
        dir.mkdir()
    pic_dir = dir / query
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
    html_num = len(list(import_html_dir.glob('*.html')))
    pic_num = len(list(pic_dir.glob('*.html')))
    size = html_num - pic_num

    csvfile = pd.read_csv(os.path.join(work_dir,f'{query}.csv'),nrows=size)
    for i in range(size):
        title = csvfile.iloc[i,1].replace("'",' ').replace("|",'\\').replace('/','\\')
        filename = f'{title}.html'
        file = import_html_dir / filename
        tar_link = dir / query / filename.rstrip('.html')
        if not os.path.exists(tar_link):
            tar_link.mkdir()
            with open(file, encoding='utf-8') as f:
                html_content = f.read()
            imglist = []
            for reg in reg_all:
                imgre = re.compile(reg)
                imglist = re.findall(imgre, html_content)+imglist
            imglist = list(set(imglist))
            print(imglist)
            for item in imglist:
                if not item.startswith('http'):
                    item = f'http://{item}'
                try:
                    img_data = requests.get(item, headers=header).content
                    if str(filetype.guess(img_data)).count('Jpeg')>0 or str(filetype.guess(img_data)).count('Gif')>0:
                        style=re.split(r'[.\s]',str(filetype.guess(img_data)))[3].lower()
                        with open(os.path.join(tar_link, f'{uuid.uuid4().hex}.{style}'), 'w+') as f:
                            f.buffer.write(img_data)
                except:
                    print('error',filename,item)
            time.sleep(3)
