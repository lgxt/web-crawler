import pandas as pd
from pathlib import Path
import os

def key(query,key_query):
    work_dir = Path.cwd().parent / 'csv'
    data=pd.read_csv(os.path.join(work_dir,f'{query}.csv'))
    name=['title','link']
    dir_export = Path.cwd().parent / 'key' / query
    dir = Path.cwd().parent / 'key'
    if not dir.exists():
        dir.mkdir()
    if not dir_export.exists():
        dir_export.mkdir()
    for key,value in key_query.items():
        final_content_list = []
        for i in value:
            for ii in range(len(data)):
                title = data.iloc[ii, 1]
                link = data.iloc[ii, 2]
                if title.count(i) > 0:
                    print(title, i)
                    final_items = []
                    final_items.append(title)
                    final_items.append(link)
                    final_content_list.append(final_items)
            print(final_content_list)
        test = pd.DataFrame(columns=name, data=final_content_list)
        test = test.drop_duplicates(['title'])
        test.to_csv(os.path.join(dir_export, "{}.csv".format(key)), mode='a', encoding='utf-8-sig')