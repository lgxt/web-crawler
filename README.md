# web-crawler
5/25-5/30爬虫代码
author：金方明

**注意事项**
用于从微信上爬取文章连接，下载html，图片以及进行关键词筛选，下载文件夹并保存至project路径即可使用py文档中函数
需要一个微信公众号以及可以扫码的手机

需使用代理ip，自动从网上获取免费ip并组装ip池，按以下链接操作：https://github.com/Python3WebSpider/ProxyPool
query为微信公众号名称

**获取url以及title**，文件自动保存至python运行路径下的csv文件夹

automatic.automatics(query)

**获取html**，文件自动保存至python运行路径下的html文件夹中的query子文件夹

download_html.downloads(query)

**html转化为md**，文件自动保存至python运行路径下的md文件夹中的query子文件夹

pandoc.htmltomd(query)

**html中图片下载**，文件自动保存至python运行路径下的pic文件夹中的query子文件夹,按照照片所在html分类放置

extract_pic.extract_pic('中土红皮书')

**根据标题进行关键词筛选**，文件自动保存至python运行路径下的key文件夹

key_word.key(query,key_query)

key_query格式 eg：key_query={'魔戒':{'魔戒','指环王','三部曲'},'霍比特人':{'霍比特人','五军之战','五军','霍比特'}}

**根据文章内容进行关键词筛选**，文件自动保存至python运行路径下的category文件夹

contain_extract.contain_word(query,key_query)


