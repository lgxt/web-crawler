import urllib.request
import pandas as pd
import os
import sys
import socket
from time import time
import threading
import random
from fake_useragent import UserAgent
import os
from pathlib import Path
import time

def downloads(query,sleeps=6,download_all = False):
    work_dir = Path.cwd().parent / 'csv'
    export_dir = Path.cwd().parent / 'html'
    if not export_dir.exists():
        export_dir.mkdir()
    html_export = export_dir / f'{query}'
    if not export_dir.exists():
        export_dir.mkdir()
    num = len(list(html_export.glob('*.html')))
    print(num)
    # 导入目标csv并分割
    file = pd.read_csv(os.path.join(work_dir, f'{query}.csv'))
    print(len(file))
    size = len(file)-num

    if size>=100:
        size_chuck = size//4
        size_residual = size%4
        data = pd.read_csv(os.path.join(work_dir,f'{query}.csv'),nrows=size,chunksize=size_chuck)
        for i, chuck in enumerate(data):
            chuck.to_csv(os.path.join(work_dir,'out{}_{}.csv'.format(i,query)),encoding='utf-8-sig')
        data0 = pd.read_csv(os.path.join(work_dir,f'out0_{query}.csv'))
        data1 = pd.read_csv(os.path.join(work_dir,f'out1_{query}.csv'))
        data2 = pd.read_csv(os.path.join(work_dir,f'out2_{query}.csv'))
        data3 = pd.read_csv(os.path.join(work_dir,f'out3_{query}.csv'))
        if size_residual != 0:
            data4 = pd.read_csv(os.path.join(work_dir,f'out4_{query}.csv'))
    elif size<100 and size>0:
        data = pd.read_csv(os.path.join(work_dir,f'{query}.csv'),nrows=size)

    def download(data, query):
        html_export = export_dir / f'{query}'
        for i in range(size):
            # url为链接，id为标题
            if size > 100:
                url = data.iloc[i, 3]
                print(data.iloc[i, 2],url)
                id = data.iloc[i, 2].replace("'",' ').replace("|",'\\').replace('/','\\')
            elif size<100 and size>0:
                url = data.iloc[i, 2]
                id = data.iloc[i, 1].replace("'",' ').replace("|",'\\').replace('/','\\')
            # 读取目标url
            path = html_export / f'{id}.html'
            if not os.path.exists(path):
                print(id)
                try:
                    ua = UserAgent().random
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', ua)]
                    urllib.request.install_opener(opener)
                    response = urllib.request.urlopen(url, timeout=120)
                    content = response.read()
                    response.close()
                    time.sleep(sleeps)
                except urllib.error.URLError as e:
                    print(type(e), id)
                except socket.timeout as e:
                    print(type(e), id)
                # 保存至本地
                path = html_export / '{}.html'.format(id)
                with open(path, 'wb') as code:
                    code.write(content)

    if size >= 100:
        # 多线程
        t1 = threading.Thread(target=download, args=(data0, query))
        t2 = threading.Thread(target=download, args=(data1, query))
        t3 = threading.Thread(target=download, args=(data2, query))
        t4 = threading.Thread(target=download, args=(data3, query))
        if size_residual != 0:
            t5 = threading.Thread(target=download, args=(data4, query))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        if size_residual != 0:
            t5.start()
        # 等待两个子线程结束再结束主线程
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        if size_residual != 0:
            t5.join()
        os.remove(os.path.join(work_dir, f'out0_{query}.csv'))
        os.remove(os.path.join(work_dir, f'out1_{query}.csv'))
        os.remove(os.path.join(work_dir, f'out2_{query}.csv'))
        os.remove(os.path.join(work_dir, f'out3_{query}.csv'))
        if size_residual != 0:
            os.remove(os.path.join(work_dir, f'out4_{query}.csv'))
    elif size<100 and size>0:
        download(data, query)
    elif size == 0:
        print('下载已完毕')
