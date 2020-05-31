# -*- coding: utf-8 -*-
import requests
import time
import csv
import pandas as pd

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
# 公众号名字
query='鲁法行谈'

# 使用Cookie，跳过登陆操作(手动在网页获取信息) 以下header已过期，作为参考
headers = {
  "Cookie": "noticeLoginFlag=1; pgv_pvid=6168959410; pac_uid=0_5e6ba4f5301b5; pgv_pvi=99416064; pgv_si=s3599769600; RK=tXplUifXSQ; ptcz=12c561d4848774295dcd7e19491a52a05c8edbb28b80099b042df42c19cdb151; pgv_info=ssid=s2241316272; rewardsn=; wxtokenkey=777; ua_id=AXaFb0kagRdeFSyvAAAAACMZSVruDilhKVWPFoqZays=; cert=gccKP_Y88zMvIj1lpu4AiucitAnykho1; uuid=ac12db09c78f7ae5110a0d79d7adadf4; bizuin=3280783256; ticket=7b6971cf025e98444c585a40ffcb7309bd080f2b; ticket_id=gh_f66c967e2ca5; rand_info=CAESIPcNP344hjjH3JEItvm5CYq3iAHOsYfkeSCxAr3nc1YB; slave_bizuin=3280783256; data_bizuin=3280783256; data_ticket=BW9bp0LPHDfJIDDHN+HIz3aNAbDxa0aFKNMJ7MG1wcEjZmnA0TWiuX1DQUFNabeV; slave_sid=dGphdGcyOWRZbWhkQmZMd3YzdHM4NUsydzJHbnVOZDNuRGZVTmc0TWtUamlzNTBEMFBEWFRBdTF5eE5sUndVVGZleG5pS3pEWnV2R1NidGhiaG52bDZCbldLR1VtaGV4bmp5WW82RTBXaTJqTlJUeEltZGdobHY5ZWlKMkg0UmczZU9tMWZlaVlXVkxqUjlu; slave_user=gh_f66c967e2ca5; xid=c72408b8ecbc793610861538e7007ece; openid2ticket_omMeMw5oTFafVF2WYNMLtKfUAaZo=tuESkCBuKTEIgBvYY3rTtocaQgR0vTyuj2zB50Agmc0=; mm_lang=zh_CN",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

data = {
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "fakeid": "MzUxNjYwMjA0OA==",
    "type": "9",
    "query": "",
    "token": "1665160340",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
}

content_list = []
for i in range(20):
    data["begin"] = i*5
    time.sleep(3)
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
    # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        content_list.append(items)
    print(i)
name=['title','link']
test=pd.DataFrame(columns=name,data=content_list)
test = test.drop_duplicates(['title'])
test.to_csv("{}.csv".format(query),mode='a',encoding='utf-8-sig')
print("保存成功")



