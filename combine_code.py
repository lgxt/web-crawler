import sys
import automatic
import download_html
import extract_pic
import pandoc
import key_word
import contain_extract
import pandas as pd
from pathlib import Path
import time
import random

dir = Path.cwd().parent / '公众号.csv'
account=pd.read_csv(dir)
for i in range(len(account)):
    account_id = account.iloc[i,0]
    certification = account.iloc[i,1]
    trademark = account.iloc[i,2]
    category = account.iloc[i,3]
    if trademark == 1:
        automatic.automatics(account_id)
        time.sleep(random.randint(180,300))
# key_query={'魔戒':{'魔戒','指环王','三部曲'},'霍比特人':{'霍比特人','五军之战','五军','霍比特'}}
#for query in query_list:
#    automatic.automatics(query)
# 获取url以及title
# automatic.automatics(query)
# 获取html
# download_html.downloads(query)
# html转化为md
# pandoc.htmltomd(query)
# html中图片下载
# extract_pic.extract_pic('中土红皮书')
# 根据标题进行关键词筛选
# key_word.key(query,key_query)
# 根据文章内容进行关键词筛选
# contain_extract.contain_word(query,key_query)
