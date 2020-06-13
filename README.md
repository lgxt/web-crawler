# web-crawler
5/25-5/30爬虫代码
author：金方明

**依赖包**
requests
json
fake_useragent
pandas 
pathlib 
urllib
socket
textrank4zh
jieba 
bs4 
codecs
threading
uuid
re
filetype
csv
numpy
pandoc（使用brew安装）

**注意事项**
用于从微信上爬取文章连接，下载html，图片以及进行关键词筛选，下载文件夹并保存至project路径即可使用py文档中函数
需要一个微信公众号以及可以扫码的手机

需使用代理ip，自动从网上获取免费ip并组装ip池，按以下链接操作：https://github.com/Python3WebSpider/ProxyPool
query为微信公众号名称

**获取url以及title**，文件自动保存至python运行路径下的csv文件夹(sleep休眠时间，建议在3分钟(sleep=180)以上）

automatic.automatics(query_list,sleeps)

**获取html**，文件自动保存至python运行路径下的html文件夹中的query子文件夹(sleep休眠时间，建议在20秒-30秒及以上，或者可设置为0，但是只能最多下载1500篇）

download_html.downloads(query,sleeps)

**html转化为md**，文件自动保存至python运行路径下的md文件夹中的query子文件夹

pandoc.htmltomd(query)

**html中图片下载**，文件自动保存至python运行路径下的pic文件夹中的query子文件夹,按照照片所在html分类放置

extract_pic.extract_pic('中土红皮书')

**参数筛选**

范例文件：category.csv，已进行手动文本分类

1.限定某个分类，将文件内url对应文章分词，确定分词频率(path为category范例文件储存路径，文件自动保存至python运行路径下的category文件夹，名字为word_freq.csv

freq_word.freq_word(path,category) 

3.确定分词在同分类所有文章中的出现频率(文件自动保存至python运行路径下的category文件夹，名字为intersect_freq.csv）

freq_word.intersect(category)

2.寻找每个分类具有特异性的标签(文件自动保存至python运行路径下的category文件夹，名字为specific_tag.csv）

freq_word.category_special_tag(ratio)

根据以上结果以及手动筛选经验确定不同分类的关键词，尝试使用上述关键词分类样本文件并选择合适参数

3.统计文章中不同分类关键词出现的次数,输入文件为

parameter.category_train(path,title_tag,tag)

4.分类（可手动筛选参数：k1,n2,n3，具体含义见文档）

parameter.predict_train(title_tag,tag,k1,n2,n3)

**根据标题及文章内容进行关键词分类**，文件自动保存至python运行路径下的category文件夹

predict.category(query,tag,title_tag)

predict.predict(query,tag,title_tag,k1,n2,n3)

tag（用于正文筛选）title_tag（用于正文筛选）格式如下：

    # 在线直播
    title1 = ['直播']
    
    # 企业合作
    title2 = ['携手','协助','合作','联合','加盟','协议','签署','签约','联手','牵手','案例']
    
    # 活动会议
    title3 = ['会议','峰会','会场','大会','活动','举行','举办','开幕','训练']
    
    # 新品上市
    title4 = ['新品','发布','推出','开放','上线']
    
    title_tag = {'在线直播':title1,'企业合作':title2,'活动会议':title3,'新品上市':title4}

**使用jieba提取关键词并分类效果较差，已放弃维护key_word以及contain_extract两个程序**

