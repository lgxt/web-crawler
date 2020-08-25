# -*-coding:utf-8 -*-
import os
import csv
import codecs
import jieba
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

# 用于标题筛选
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

# 统计不同文章中不同分类关键词出现的次数
def category(query,tag,title_tag):
    import_csv_dir = Path.cwd().parent / 'csv' / f'{query}.csv'
    output_csv_dir = Path.cwd().parent / 'category'
    if not output_csv_dir.exists():
        output_csv_dir.mkdir()
    csv_import = pd.read_csv(import_csv_dir)
    output_csv_dir = output_csv_dir / f'{query}.csv'

    if output_csv_dir.exists():
        num = len(pd.read_csv(output_csv_dir))
        title_list = list(pd.read_csv(import_csv_dir)['title'])
        size = len([x for x in title_list if not pd.isnull(x)])-num
        print(num,len([x for x in title_list if not pd.isnull(x)]),size)
    else:
        size = len(csv_import)

    word_final = []
    for i in range(size):
        try:
            title = csv_import.iloc[i,1]
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
            word_intersect.append(csv_import.iloc[i,2])

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
            word_final.append(word_intersect)
        except:
            print('error', title, query)

    if output_csv_dir.exists():
        previous = pd.read_csv(output_csv_dir).values
        with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
            write = csv.writer(f, dialect='excel')
            write.writerow(['title', 'link', '在线直播t',"企业合作t", "活动会议t",'新品上市t',"在线直播",'tag1',"企业合作", 'tag2', "活动会议",'tag3', '新品上市','tag4','predict'])
            for item in previous:
                write.writerow(item)
            for item in word_final:
                write.writerow(item)
    else:
        with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
            write = csv.writer(f, dialect='excel')
            write.writerow(['title', 'link', '在线直播t',"企业合作t", "活动会议t",'新品上市t',"在线直播",'tag1',"企业合作", 'tag2', "活动会议",'tag3', '新品上市','tag4'])
            for item in word_final:
                write.writerow(item)
    return size

#for query in ['SAP中国顾问公众平台','SAP会员服务','SAP天天事','SAP成长型企业社区','金蝶','金蝶K3','金蝶KIS','金蝶云服务','阿里云','阿里研究院']:
    #category(query,tag,title_tag)

# 利用训练集进行参数选择
# 根据之前predict.csv的结果预测并输出预测结果，可以选择参数
def predict(query,k1,k2,n2,n3,n4,n5):
    import_csv_dir = Path.cwd().parent / 'category' / f'{query}.csv'
    output_csv_dir = import_csv_dir
    csv_import = pd.read_csv(import_csv_dir)
    category_list = []
    for i in range(len(csv_import)):
        row = list(csv_import.iloc[i,0:14])
        print(row)
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
            print(csv_import['新品上市'][i],csv_import['企业合作'][i],csv_import['活动会议'][i])
            if csv_import['新品上市'][i] + csv_import['企业合作'][i] + csv_import['活动会议'][i] > 0:
                fraction = csv_import['企业合作'][i] / (csv_import['新品上市'][i] + csv_import['企业合作'][i] + csv_import['活动会议'][i])
                fraction2 = csv_import['活动会议'][i] / (csv_import['新品上市'][i] + csv_import['企业合作'][i] + csv_import['活动会议'][i])
            else:
                fraction = 0
                fraction2 = 0
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
                            category = ' '
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
                            category = ' '

        row.append(category)
        category_list.append(row)

    with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
        write = csv.writer(f, dialect='excel')
        write.writerow(['title', 'link', '在线直播t', "企业合作t", "活动会议t", '新品上市t', "在线直播", 'tag1', "企业合作", 'tag2', "活动会议", 'tag3','新品上市', 'tag4', 'predict'])

        for item in category_list:
            write.writerow(item)
