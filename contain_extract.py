#-*- encoding:utf-8 -*-
from __future__ import print_function
import sys
from bs4 import BeautifulSoup
import codecs
from textrank4zh import TextRank4Keyword
from jieba import analyse
from pathlib import Path
import pandas as pd
import os
from shutil import copyfile
import csv

# 使用jieba，textrank4zh提取关键词
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

# 载入html
def contain_word(query,key_query):
    import_html_dir = Path.cwd().parent / 'html' / query
    index_csv_dir = Path.cwd().parent / 'csv' / f'{query}.csv'
    export_dir = Path.cwd().parent / 'category'
    if not export_dir.exists():
        export_dir.mkdir()
    export_html_dir = Path.cwd().parent / 'category' / query
    if not export_html_dir.exists():
        export_html_dir.mkdir()
    index = pd.read_csv(index_csv_dir)

    for key, value in key_query.items():
        with open(os.path.join(f'{key}.csv'), 'w',encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["title", "url"])

    for i in range(len(index)):
        url = index.iloc[i,2]
        title = index.iloc[i,1]
        html_file = codecs.open(os.path.join(import_html_dir,f'{title}.html'), 'r', 'utf-8').read()
        end = 'media_tool_meta tips_global_primary meta_primary'
        html_file = html_file[:html_file.rfind(end)]
        text = BeautifulSoup(html_file,features="lxml").get_text() #转化为txt
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=text, lower=True, window=2)
        list_key = []
        for key_word in tr4w.get_keywords(10, word_min_len=2):
            list_key.append(key_word.word)
        textrank = analyse.textrank
        keywords = textrank(text, 10)
        for keyword in keywords:
            list_key.append(keyword)
        list_key = set(list_key)
        print(title,list_key)
        for key, value in key_query.items():
            if not list_key.isdisjoint(value):
                print(title,key)
                with open(os.path.join(export_html_dir,f'{key}.csv'), 'a',encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([(title, url)])








