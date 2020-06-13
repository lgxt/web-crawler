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
# query_list = ["中土红皮书","精灵宝钻"]

# 获取url以及title
# automatic.automatics(query_list,sleeps)

# 获取html
# download_html.downloads(query,sleeps)

# html转化为md
# pandoc.htmltomd(query)

# html中图片下载
# extract_pic.extract_pic('中土红皮书')

# 根据标题进行关键词筛选
# key_word.key(query,key_query)

# 根据文章内容进行关键词筛选
# contain_extract.contain_word(query,key_query)

#参数筛选
#范例文件：category.csv，已进行手动文本分类
#1.限定某个分类，将文件内url对应文章分词，确定分词频率(path为category范例文件储存路径，文件自动保存至python运行路径下的category文件夹，名字为word_freq.csv
#freq_word.freq_word(path,category)
#3.确定分词在同分类所有文章中的出现频率(文件自动保存至python运行路径下的category文件夹，名字为intersect_freq.csv）
#freq_word.intersect(category)
#2.寻找每个分类具有特异性的标签(文件自动保存至python运行路径下的category文件夹，名字为specific_tag.csv）
#freq_word.category_special_tag(ratio)

#根据以上结果以及手动筛选经验确定不同分类的关键词，尝试使用上述关键词分类样本文件并选择合适参数
#3.统计文章中不同分类关键词出现的次数,输入文件为
#parameter.category_train(path,title_tag,tag)
#4.分类（可手动筛选参数：k1,n2,n3，具体含义见文档）
#parameter.predict_train(title_tag,tag,k1,n2,n3)

#根据标题及文章内容进行关键词分类，文件自动保存至python运行路径下的category文件夹
#predict.category(query,tag,title_tag)
#predict.predict(query,tag,title_tag,k1,n2,n3)
