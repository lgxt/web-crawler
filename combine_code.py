import automatic
import download_html
import extract_pic
import predict
import nlp
from pathlib import Path
import pandas as pd
pd.set_option('max_colwidth',1000)
import send_msg
import os

checkFile = Path.cwd().parent / "isRunning.txt"
with open(checkFile, 'w') as file:
    file.write('isrunning')   

#公众号名称
query_list = ['SAP中国顾问公众平台','SAP会员服务','SAP天天事','SAP成长型企业社区','金蝶','金蝶K3','金蝶KIS','金蝶云服务','阿里云','阿里研究院']

# 用于文章（标题）分类

# 在线直播
title1 = ['直播']
# 企业合作
title2 = ['携手','协助','合作','联合','加盟','协议','签署','签约','联手','牵手','案例']
# 活动会议
title3 = ['会议','峰会','会场','大会','活动','举行','举办','开幕','训练']
# 新品上市
title4 = ['新品','发布','推出','开放','上线']
title_tag = {'在线直播':title1,'企业合作':title2,'活动会议':title3,'新品上市':title4}

# 用于文章（内容）分类

# 在线直播
tag1 = ['直播']
# 企业合作
tag2 = ['伙伴','仪式','启动','携手','协助','合作','联合','加盟','协议','签署','共同','签约','共建','共赢','联手','双方','牵手','效率','搭建','选择','传统','需求','解决','高效','成本','案例']
# 活动会议
tag3 = ['会议','峰会','会场','大会','议程','参加','活动','举行','致辞','主办','举办','邀请','探讨','参会','现场','讲座','日程','出席','开幕','训练',]
# 新品上市
tag4 = ['新品','解决方案','助力','咨询热线','发布','全新','推出','开放','上线']
tag = {'在线直播':tag1,'企业合作':tag2,'活动会议':tag3,'新品上市':tag4}

SENDER = 'YNWAGeorge@163.com'
SMTP_SERVER = 'smtp.163.com'
USER_ACCOUNT = {'username':'YNWAGeorge@163.com', 'password':''}
receivers = ['enelothe@gmail.com']

automatic.automatics(query_list)
sizes = []
for query in query_list:
    download_html.downloads(query)
    extract_pic.extract_pic(query)
    size_new = predict.category(query, tag, title_tag) #文章分类，输出size
    print(size_new)
    predict.predict(query,0.7,0.5,1,9,0,4)
    #nlp.nlp(query)
    sizes.append(size_new)
send_msg.send_mail(query_list,sizes=sizes)

os.remove(checkFile)

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
