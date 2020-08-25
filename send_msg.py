import csv
import codecs
from pathlib import Path
import pandas as pd
pd.set_option('max_colwidth',1000)
import time
import yagmail
import os

#query_list = ['SAP中国顾问公众平台','SAP会员服务','SAP天天事','SAP成长型企业社区','金蝶','金蝶K3','金蝶KIS','金蝶云服务','阿里云','阿里研究院']

def send_mail(query_list,sizes):
    for i in range(len(query_list)):
        query = query_list[i]
        size = sizes[i]
        import_path = Path.cwd().parent / 'category' / f'{query}.csv'
        text = pd.read_csv(import_path).tail(size)
        text['query'] = query
        for subject in ['企业合作','活动会议']:
            text1 = text[text['predict'] == subject].iloc[:,[0,1,15]].values
            print(text1)
            output_path = Path.cwd().parent / 'category' / f'{subject}.csv'
            with codecs.open(filename=output_path, mode='a', encoding='utf-8-sig')as f:
                write = csv.writer(f, dialect='excel')
                if i == 0:
                    write.writerow(['title','link','query'])
                for item in text1:
                    write.writerow(item)
                   
'''
    path1 = '/Users/fangmingjin/PycharmProjects/web_spider/category/企业合作.csv'
    path2 = '/Users/fangmingjin/PycharmProjects/web_spider/category/活动会议.csv'
    subject = '微信分类' + ' ' + time.strftime("%Y-%m-%d", time.localtime())
    yag = yagmail.SMTP(user='******@gmail.com',password='******',host='smtp.gmail.com')
    yag.send(to='enelothe@gmail.com',subject=subject,contents=['今日微信文章分类请见附件：',path1,path2])
'''
