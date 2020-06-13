# -*-coding:utf-8 -*-
import os
import csv
import codecs
import jieba
import jieba.posseg as pseg
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

#对获得的html正文分词并求频率
def freq_word(path,category):
    import_csv_dir = path
    output_csv_dir = Path.cwd().parent / 'category'
    if not output_csv_dir.exists():
        output_csv_dir.mkdir
    csv_import = pd.read_csv(import_csv_dir)
    id = 0
    for i in range(len(csv_import)):
        if csv_import['category'][i] == category:
            id += 1
            title = csv_import['title'][i]
            query = csv_import['query'][i]
            import_html_dir = Path.cwd().parent / 'html' / query
            title = title.replace("'",' ').replace("|",'\\').replace('/','\\')
            html_file = codecs.open(os.path.join(import_html_dir,f'{title}.html'), 'r', 'utf-8').read()
            end = 'media_tool_meta tips_global_primary meta_primary'
            html_file = html_file[:html_file.rfind(end)]
            txt = BeautifulSoup(html_file,features="lxml").get_text()

            # 词频统计
            cixing = pseg.lcut(txt)
            count = jieba.lcut(txt)
            word_count = {}
            word_flag = {}
            all = []

            output_csv = output_csv_dir / 'word_freq.csv'
            ex = 'export csv exist'
            if not output_csv.exists():
                ex = 'export csv does not exist'
            with codecs.open(filename=output_csv, mode='a', encoding='utf-8-sig')as f:
                write = csv.writer(f, dialect='excel')
                if id == 1 and ex == 'export csv does not exist':
                    write.writerow(['category', 'title', "word", "count", "flag"])

                # 词性统计
                for w in cixing:
                    word_flag[w.word] = w.flag

                # 词频统计
                for word in count:
                    if word not in stopwords:
                        # 不统计字数为一的词
                        if len(word) == 1:
                            continue
                        else:
                            word_count[word] = word_count.get(word, 0) + 1

                items = list(word_count.items())
                # 按词频排序
                items.sort(key=lambda x: x[1], reverse=True)
                # 查询词频字典里关键字的词性
                for i in range(len(items)):
                    word = []
                    word.append(category)
                    word.append(title)
                    word.append(items[i][0])
                    word.append(items[i][1])
                    # 若词频字典里，该关键字有分辨出词性，则记录，否则为空
                    if items[i][0] in word_flag.keys():
                        word.append(word_flag[items[i][0]])
                    else:
                        word.append("")
                    all.append(word)

                for res in all:
                    write.writerow(res)

#for category in ['客户案例','在线直播','活动会议','新品上市','企业合作']:
    #freq_word(category)

#求关键词交集
def intersect(category):
    #导入html词频文件（上一个函数freq_word获得）
    import_csv_dir = Path.cwd().parent / 'category' / 'word_freq.csv'
    output_csv_dir = Path.cwd().parent / 'category' / 'intersect_freq.csv'
    csv_import = pd.read_csv(import_csv_dir)

    list_word = []
    list_freq = []
    list_final = []

    title = []

    for i in range(len(csv_import)):
        line = []
        if csv_import['category'][i] == category:
            title.append(csv_import['title'][i])
            line.append(csv_import['word'][i])
            list_word.append(csv_import['word'][i])
            line.append(csv_import['count'][i])
            list_freq.append(line)

    title_num = len(list(set(title)))
    # 计算每一个词在所有文章中的出现次数，频率（假设分类文章数量为n，出现于m篇文章，并在m篇文章中共出现k次，计算k/n以及m/n的值）
    for word in list(set(list_word)):
        freq = 0
        count = round(list_word.count(word)/title_num,3)
        list_words = []
        for item in list_freq:
            if item[0] == word:
                freq = freq + item[1]
        freq = round(freq/title_num,3)
        list_words.append(category)
        list_words.append(word)
        list_words.append(freq)
        list_words.append(count)
        list_final.append(list_words)

    # 排序
    list_final.sort(key=lambda x: (-x[3],-x[2]))
    
    # 输出结果
    ex = 'export csv exist'
    if not output_csv_dir.exists():
        ex = 'export csv does not exist'
    with codecs.open(filename=output_csv_dir, mode='a', encoding='utf-8-sig')as f:
        write = csv.writer(f, dialect='excel')
        if ex == 'export csv does not exist':
            write.writerow(['category', "word", "freq", "count"])

        for item in list_final:
            write.writerow(item)


#for category in ['客户案例','在线直播','活动会议','新品上市','企业合作']:
    #intersect(category)

#寻找每个分类具有特异性的标签
def category_special_tag(ratio):
    import_csv_dir = Path.cwd().parent / 'category' / 'intersect_freq.csv'
    output_csv_dir = Path.cwd().parent / 'category' / 'specific_tag.csv'
    csv_import = pd.read_csv(import_csv_dir)
    # 对于多个分类，筛选出k/n>ratio的分词，并求出独属于某一分类的特异性分词
    csv_import = csv_import[csv_import['count']>=ratio]
    list_word = list(csv_import['word'])
    dict = {}

    # 统计分词在不同分类中出现频率
    for word in list(set(list_word)):
        dict[word] = list_word.count(word)

    info_combine = []
    for key, value in dict.items():
        lists = []
        freq = 0
        count = 0
        category = []
        # 记录分词在几个分类中出现过，出现的频率之和
        for i in range(len(csv_import)):
            if csv_import.iloc[i,1] == key:
                category.append(csv_import.iloc[i,0])
                freq = freq + csv_import.iloc[i,2]
                count = count + csv_import.iloc[i,3]
        lists.append(category)
        lists.append(key)
        lists.append(freq)
        lists.append(count)
        lists.append(value)
        info_combine.append(lists)

    info_combine.sort(key=lambda x: (x[0], x[4]))

    ex = 'export csv exist'
    if not output_csv_dir.exists():
        ex = 'export csv does not exist'
    with codecs.open(filename=output_csv_dir, mode='w', encoding='utf-8-sig')as f:
        write = csv.writer(f, dialect='excel')
        if ex == 'export csv does not exist':
            write.writerow(['category', "word", "freq", "count", 'duplicate'])

        for item in info_combine:
            write.writerow(item)

category_special_tag(ratio)
