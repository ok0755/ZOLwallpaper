#coding=utf-8
# ok075588
# python27

import urllib2
import urllib
import re
import requests
from bs4 import BeautifulSoup
import time
import lxml

class Getdesk(object):
    def __init__(self,start,end):
        self.re_pic=re.compile('<img src.?="(https://desk-fd.*?)" width="144" height="90"')
        self.start=start
        self.end=end
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
        self.root_url='http://desk.zol.com.cn'
        self.urls(self.start,self.end)

    def urls(self,start,end):
        for i in range(start,end):
            url='http://desk.zol.com.cn/qiche/1280x1024/{}.html'.format(i)
            self.getpage(url)

    def getpage(self,url):
        time.sleep(1)
        res=requests.get(url,self.header)
        resp=res.text
        res.close()
        soup=BeautifulSoup(resp,'lxml')
        obj_page=soup.find_all('li',class_="photo-list-padding")
        for obj in obj_page:
            self.obj(self.root_url+obj.a['href'])

    def obj(self,url):
        time.sleep(1)
        res=requests.get(url,self.header)
        resp=res.text
        res.close()
        pic_url=re.findall(self.re_pic,resp)
        for pic in pic_url:
            pic=pic.replace('144x90','1280x1024')
            self.get_content(pic,)


    def get_content(self,link):
        urllib.urlretrieve(link,'d:\\bizi\\{}{}'.format(int(time.time()*10),'.jpg'))
if __name__=='__main__':
    Getdesk(21,22)  #起始页
