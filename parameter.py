# -*-coding:utf-8 -*-
import os
import csv
import codecs
import jieba
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import numpy

# 在线直播
title1 = ['直播']
# 企业合作
title2 = ['携手','协助','合作','联合','加盟','协议','签署','签约','联手','牵手','案例']
# 活动会议
title3 = ['会议','峰会','会场','大会','活动','举行','举办','开幕','训练']
# 新品上市
title4 = ['新品','发布','推出','开放','上线']
title_tag = {'在线直播':title1,'企业合作':title2,'活动会议':title3,'新品上市':title4}

# 在线直播
tag1 = ['直播']
# 企业合作
tag2 = ['伙伴','仪式','启动','携手','协助','合作','联合','加盟','协议','签署','共同','签约','共建','共赢','联手','双方','牵手','效率','搭建','选择','传统','需求','解决','高效','成本','案例']
# 活动会议
tag3 = ['会议','峰会','会场','大会','议程','参加','活动','举行','致辞','主办','举办','邀请','探讨','参会','现场','讲座','日程','出席','开幕','训练',]
# 新品上市
tag4 = ['新品','解决方案','助力','咨询热线','发布','全新','推出','开放','上线']
tag = {'在线直播':tag1,'企业合作':tag2,'活动会议':tag3,'新品上市':tag4}

# 利用训练集进行参数选择
# 统计不同文章中不同分类关键词出现的次数
def category_train(path,title_tag,tag):
    import_csv_dir = category_train()
    output_csv_dir = Path.cwd().parent / 'category' / 'predict.csv'
    csv_import = pd.read_csv(import_csv_dir)
    word_final = []
    for i in range(len(csv_import)):
        title = csv_import['title'][i]
        query = csv_import['query'][i]
        import_html_dir = Path.cwd().parent / 'html' / query
        title = title.replace("'", ' ').replace("|", '\\').replace('/', '\\')
        html_file = codecs.open(os.path.join(import_html_dir, f'{title}.html'), 'r', 'utf-8').read()
        end = 'media_tool_meta tips_global_primary meta_primary'
        html_file = html_file[:html_file.rfind(end)]
        txt = BeautifulSoup(html_file, features="lxml").get_text()

        # 词频统计
        count = jieba.lcut(txt)
        word_count = {}

        # 词频统计
        for word in count:
            # 不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                word_count[word] = word_count.get(word, 0) + 1

        word = list(set(count))

        word_intersect = []
        word_intersect.append(title)
        word_intersect.append(csv_import['link'][i])

        #统计各个关键词在标题中出现次数
        for key, value in title_tag.items():
            n = 0
            for item in value:
                n = title.count(item) + n
            word_intersect.append(n)

        #统计各个关键词在正文中出现次数
        for key, value in tag.items():
            intersect = list(set(value).intersection(set(word)))
            freq = len(intersect)
            word_intersect.append(freq)
            word_intersect.append(intersect)
        word_intersect.append(csv_import['category'][i])
        word_final.append(word_intersect)

    with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
        write = csv.writer(f, dialect='excel')
        write.writerow(['title', 'link', '在线直播t',"企业合作t", "活动会议t",'新品上市t',"在线直播",'tag1',"企业合作", 'tag2', "活动会议",'tag3', '新品上市','tag4','category',])

        for item in word_final:
            write.writerow(item)

# 利用训练集进行参数选择
# 根据之前predict.csv的结果预测并输出预测结果，可以选择参数
def predict_train(title_tag,tag,k1,k2,n2,n3,n4,n5):
    import_csv_dir = Path.cwd().parent / 'category' / 'predict.csv'
    output_csv_dir = Path.cwd().parent / 'category' / 'predict.csv'
    csv_import = pd.read_csv(import_csv_dir)
    category_list = []
    FN = 0
    FP = 0
    TN = 0
    TP = 0
    FN2 = 0
    FP2 = 0
    TN2 = 0
    TP2 = 0
    for i in range(len(csv_import)):
        row = []
        row = list(csv_import.iloc[i,:])
        title_tag = {'在线直播': csv_import['在线直播t'][i], '企业合作': csv_import['企业合作t'][i], '活动会议': csv_import['活动会议t'][i],
                     '新品上市': csv_import['新品上市t'][i]}

        n = 0
        lists = []

        # 使用标题判断文章类型
        for key, value in title_tag.items():
            if value >= 1:
                n += 1
                lists.append(key)
        if n == 1:
            category = lists[0]
        elif n > 1:
            if lists.count('在线直播') >= 1:
                category = '在线直播'
            elif lists.count('在线直播') == 0:
                if lists.count('企业合作') >= 1:
                    category = '企业合作'
                elif lists.count('企业合作') == 0:
                    if lists.count('活动会议') >= 1:
                        category = '活动会议'
        elif n == 0:
            # 使用正文判断文章内容
            fraction = csv_import['企业合作'][i]/(csv_import['新品上市'][i]+csv_import['企业合作'][i]+csv_import['活动会议'][i])
            fraction2 = csv_import['活动会议'][i] / (csv_import['新品上市'][i] + csv_import['企业合作'][i] + csv_import['活动会议'][i])
            if csv_import['在线直播'][i] >= 1:
                category = '在线直播'
            elif csv_import['在线直播'][i] == 0:
                if fraction >= k1:
                    if csv_import['企业合作'][i] >= n2:
                        category = '企业合作'
                    elif csv_import['企业合作'][i] < n2:
                        if fraction2 >= k2 and csv_import['企业合作'][i] >= n4:
                            category = '活动会议'
                        elif fraction2 < k2 and csv_import['企业合作'][i] >= n5:
                            category = '活动会议'
                        elif fraction2 >= k2 and csv_import['企业合作'][i] < n4 and csv_import['新品上市'][i] >= 2:
                            category = '新品上市'
                        elif fraction2 < k2 and csv_import['企业合作'][i] >= n5 and csv_import['新品上市'][i] >= 2:
                            category = '新品上市'
                        else:
                            category = ''
                if fraction < k1:
                    if csv_import['企业合作'][i] >= n3:
                        category = '企业合作'
                    elif csv_import['企业合作'][i] < n3:
                        if fraction2 >= k2 and csv_import['企业合作'][i] >= n4:
                            category = '活动会议'
                        elif fraction2 < k2 and csv_import['企业合作'][i] >= n5:
                            category = '活动会议'
                        elif fraction2 >= k2 and csv_import['企业合作'][i] < n4 and csv_import['新品上市'][i] >= 2:
                            category = '新品上市'
                        elif fraction2 < k2 and csv_import['企业合作'][i] >= n5 and csv_import['新品上市'][i] >= 2:
                            category = '新品上市'
                        else:
                            category = ''

        if category == '企业合作' and csv_import['category'][i] == '企业合作':
            TP += 1
        elif category != '企业合作' and csv_import['category'][i] != '企业合作':
            TN += 1
        elif category == '企业合作' and csv_import['category'][i] != '企业合作':
            FP += 1
        elif category != '企业合作' and csv_import['category'][i] == '企业合作':
            FN += 1

        if category == '活动会议' and csv_import['category'][i] == '活动会议':
            TP2 += 1
        elif category != '活动会议' and csv_import['category'][i] != '活动会议':
            TN2 += 1
        elif category == '活动会议' and csv_import['category'][i] != '活动会议':
            FP2 += 1
        elif category != '活动会议' and csv_import['category'][i] == '活动会议':
            FN2 += 1
        row.append(category)
        category_list.append(row)
    print(TP,TN,FP,FN,TP2,TN2,FP2,FN2)
    specificity = TN/(FP+TN)
    sensitivity = TP/(TP+FN)
    specificity2 = TN2 / (FP2 + TN2)
    sensitivity2 = TP2 / (TP2 + FN2)
    return k1,k2,n2,n3,n4,n5,sensitivity,specificity,sensitivity2,specificity2

    '''
    with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
        write = csv.writer(f, dialect='excel')
        write.writerow(
            ['title', 'link', '在线直播t', "企业合作t", "活动会议t", '新品上市t', "在线直播", 'tag1', "企业合作", 'tag2', "活动会议", 'tag3',
            '新品上市', 'tag4', 'category', 'predict'])

        for item in category_list:
            write.writerow(item)
    '''

#帮助测试参数
output_csv_dir = Path.cwd().parent / 'category' / 'roc.csv'
rows = []
for k1 in [0.5,0.6,0.7,0.8]:
    for n2 in [0,1,2,3,4,5]:
        for n3 in [4,5,6,7,8,9]:
            if n3>n2:
                for k2 in [0.5,0.6,0.7,0.8]:
                    for n4 in [0,1,2,3,4,5]:
                        for n5 in [4,5,6,7,8,9]:
                            if n5 > n4:
                                row = []
                                row = list(predict_train(title_tag,tag,k1,k2,n2,n3,n4,n5))
                                rows.append(row)
with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
    write = csv.writer(f, dialect='excel')
    write.writerow(['k1','k2','n2','n3','n4','n5','sensitivity','specifity','sensitivity2','specifity2'])
    for item in rows:
        write.writerow(item)

#参数筛选
'''
最佳结果
k1              0.700000
k2              0.500000
n2              1.000000
n3              9.000000
n4              0.000000
n5              4.000000
企业合作
sensitivity     0.800000
specifity       0.848214
活动会议
sensitivity     0.712121
specifity      0.705202
趋向于选择使企业合作准确度更高
'''
output_csv_dir = Path.cwd().parent / 'category' / 'roc.csv'
roc = pd.read_csv(output_csv_dir)
for i in range(len(roc)):
    if roc.iloc[i,6]>0.7 and roc.iloc[i,7]>0.7 and roc.iloc[i,8]>0.7 and roc.iloc[i,9]>0.7:
        print(roc.iloc[i,])
