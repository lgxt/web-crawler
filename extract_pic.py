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
    import_html_dir = work_dir / 'try' / query
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
        if not tar_link.exists():
            tar_link.mkdir()
        with open(file, encoding='utf-8') as f:
            html_content = f.read()
        for reg in reg_all:
            imgre = re.compile(reg)
            imglist = re.findall(imgre, html_content)
            print(imglist)
            for item in imglist:
                img_data = requests.get(item, headers=header).content
                if str(filetype.guess(img_data)).count('Jpeg')>0 or str(filetype.guess(img_data)).count('Gif')>0:
                    style=re.split(r'[.\s]',str(filetype.guess(img_data)))[3].lower()
                    with open(os.path.join(tar_link, f'{uuid.uuid4().hex}.{style}'), 'w+') as f:
                        f.buffer.write(img_data)
                time.sleep(3)