"""
依赖的包：pyltp（安装环境：python3.6版本或以下）
使用pylyp对txt中的公司名进行识别，需要安装pyltp，安装方法参考https://www.jianshu.com/p/9518b5cf325a
需要下载ltp模型，运行代码时，需将pyltp_ner函数中将路径改为ltp模型的存放路径
"""

import os
import csv
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import logging
from pathlib import Path
import pandas as pd
import codecs
import pandas as pd

def get_txt_data(path):  # 读取txt文件
    new_lines = ""
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                line = line.replace("/n", "")
                new_lines = new_lines + line
    return new_lines


def save_data(company, path, p, t):  # 将每个文件识别出的公司名实时写入csv文件
    company_list = [[p, t, i] for i in company]
    with open(path, "a", newline='',encoding = 'utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(company_list)
        csvfile.close()


def pyltp_ner(text):  # 识别机构名-pyltp
    LTP_DATA_DIR = Path.cwd().parent / 'ltp_model'# ltp模型存放路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # 分词
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = segmentor.segment(text)  # 分词
    words_list = list(words)  # words_list列表保存着分词的结果
    segmentor.release()  # 释放模型

    # 词性标注
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    postags_list = list(postags)  # postags_list保存着词性标注的结果
    postagger.release()  # 释放模型

    # 命名体识别
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    netags_list = list(netags)  # netags_list保存着命名实体识别的结果
    data = {"reg": netags, "words": words, "tags": postags}
    # print(data)
    recognizer.release()  # 释放模型

    # 去除非命名实体
    a = len(words_list)
    words_list_1 = []
    postags_list_1 = []
    netags_list_1 = []
    for i in range(a):
        if netags_list[i] != 'O':
            words_list_1.append(words_list[i])
            postags_list_1.append(postags_list[i])
            netags_list_1.append(netags_list[i])

    # 提取机构名
    a1 = len(words_list_1)
    organizations = []
    for i in range(a1):
        if netags_list_1[i] == 'S-Ni':
            organizations.append(words_list_1[i])
        elif netags_list_1[i] == 'B-Ni':
            temp_s = ""
            temp_s += words_list_1[i]
            j = i + 1
            while j < a1 and (netags_list_1[j] == 'I-Ni' or netags_list_1[j] == 'E-Ni'):
                temp_s += words_list_1[j]
                j = j + 1
            organizations.append(temp_s)
    orignizations = list(set(organizations))  # 对公司名去重
    return orignizations

def nlp(query):
    import_csv_dir = Path.cwd().parent / 'category' / f'{query}.csv'
    output_csv_path = Path.cwd().parent / 'company'
    if not output_csv_path.exists():
        output_csv_path.mkdir()
    output_csv_path = output_csv_path / f'{query}.csv'
    csv_import = pd.read_csv(import_csv_dir)
    if output_csv_path.exists():
        exitindex = '存在该文件'
        num_csv = len(csv_import[csv_import['predict'] == '企业合作']['title'])
        company_end = pd.read_csv(output_csv_path).tail(1).iloc[0,1]
        print(company_end)
        for i in range(len(csv_import)):
            if csv_import.iloc[i,0] == company_end:
                print(csv_import.iloc[i, 0])
                num_company = i+1
        start_line = num_company
        end_line = num_csv
    else:
        exitindex = '不存在该文件'
        start_line = 0
        end_line = len(csv_import[csv_import['predict'] == '企业合作']['title'])

    company_list = []
    for i in range(start_line,end_line):
        if csv_import['predict'][i] == '企业合作':
            lists = []
            title = csv_import.iloc[i, 0]
            import_html_dir = Path.cwd().parent / 'html' / query
            title = title.replace("'", ' ').replace("|", '\\').replace('/', '\\')
            path = import_html_dir / f'{title}.html'
            text = get_txt_data(path)
            p = query
            company = pyltp_ner(text)
            lists = [[p, title, i] for i in company]
            company_list = company_list + lists
            print(company_list)
    savepath = output_csv_path
    if output_csv_path.exists():
        previous = pd.read_csv(savepath).values
        with codecs.open(filename=savepath, mode='w', encoding='utf-8-sig')as f:
            write = csv.writer(f, dialect='excel')
            write.writerow(['query','title', 'company'])
            for item in previous:
                write.writerow(item)
            for item in company_list:
                write.writerow(item)
    else:
        with codecs.open(filename=savepath, mode='w', encoding='utf-8-sig')as f:
            write = csv.writer(f, dialect='excel')
            write.writerow(['query','title', 'company'])
            for item in company_list:
                write.writerow(item)
