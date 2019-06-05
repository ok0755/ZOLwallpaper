#coding=utf-8
# ok075588
# python2.7
import re
import os
import requests
from lxml import etree
import time
from random import randint
import gevent                                                 ## 协程并发
from gevent import monkey,pool
monkey.patch_all()

class Getdesk(object):
    def __init__(self):#,start,end):
        self.re_pic=re.compile('<img src.?="(https://desk-fd.*?)" width="144" height="90"')
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        self.root_url='http://desk.zol.com.cn'
    ## 起止页
    def urls(self,start,end):
        urls=[]
        for i in range(start,end):
            url='http://desk.zol.com.cn/qiche/good_{}.html'.format(i) ## 起止页
            urls.append(url)
        return urls
    ##
    def getpage(self,url):
        time.sleep(1)
        arr=[]
        res=requests.get(url,self.header)
        resp=res.text
        res.close()
        selectors = etree.HTML(resp)
        obj_page = selectors.xpath('.//li[@class="photo-list-padding"]/a/@href')
        arr=['http://desk.zol.com.cn{}'.format(obj) for obj in obj_page]
        return arr

    def pic_urls(self,url):
        time.sleep(1)
        res=requests.get(url,self.header)
        resp=res.text
        res.close()
        html = etree.HTML(resp)
        obj_pics = html.xpath('.//img/@srcs')
        pics = [x.replace('144x90','1280x1024') for x in obj_pics]
        return pics

def collection():
    paper = Getdesk()  #起始页
    pages = paper.urls(1,31)
    for p in pages:
        for pp in paper.getpage(p):
            target_pic_urls = paper.pic_urls(pp)
            yield target_pic_urls

def download(pic):
    print('Downloading >>  ',pic)
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    r=requests.get(pic,headers=header)
    content=r.content
    r.close()
    fname = os.path.split(pic)[1]
    filename = r'd:\bizi2\{}'.format(fname)
    with open(filename, "wb+") as jpg:
        jpg.write(content)

if __name__=='__main__':
    pics = collection()
    p = pool.Pool(30)
    for urls in pics:
        for url in urls:
            th = []
            th.append(gevent.spawn(download,url))
        gevent.joinall(th,timeout=3)



