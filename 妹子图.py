#encoding:utf8

import urllib2 as request
import time
import requests
from lxml import etree
class MeiM:
    def __init__(self):
        self.root_url = "http://www.mzitu.com/"
        self.page = "http://www.mzitu.com/page/"

    def sumPage(self):#妹子图网所有的页数
        xpath = etree.HTML(request.urlopen(self.root_url).read().decode("utf8"))
        return xpath.xpath('//*[@class="nav-links"]/a[last()-1]/text()')[0]

    def sumImg(self,url):#该图集所有的页数
        xpath = etree.HTML(self.get_html(url))
        return xpath.xpath('//*[@class="pagenavi"]/a[last()-1]/span/text()')[0]

    def get_html(self,url):#获取网页源码
        # print("睡眠等待中")
        # time.sleep(1)
        if url is None:
            return None
        html = request.urlopen(url)
        if html.getcode() != 200:
            return None
        return html.read().decode("utf8")

    def img_link(self,url):#获取该页面的图片
        xpath = etree.HTML(self.get_html(url))
        return xpath.xpath('//*[@class="main-image"]/p/a/img/@src')[0]

    def download(self,url):#下载图片
        response = requests.get(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3831.211 Safari/537.36","Referer":"http://www.mzitu.com/"},timeout=5).content
        with open("img/%s"%url[-10:],"wb") as f:
            f.write(response)
        # with open("img.jpg", "wb") as f:
        #     f.write(response)
        print("已存入")

    def parse_index(self,response):#获取该页面所有的图集url
        xpath = etree.HTML(response)
        return xpath.xpath('//*[@id="pins"]/li/a/@href')

    def dio(self):
        b = []
        urls = [self.page+str(i) for i in range(1,int(self.sumPage())+1)]#获取妹子网所有网页的url
        for i in reversed(urls):
            b.append(i)
        while True:
            try:
                if urls == []:
                    print("666完成666")
                    return
                for tuji_link in self.parse_index(self.get_html(b.pop())):  # 每次爬取一页的所有图集的url
                    for page in range(1, int(self.sumImg(tuji_link))):  # 获取该图集的最大页数并循环
                        print("睡眠等待中")
                        time.sleep(1)
                        self.download(self.img_link(tuji_link + "/" + str(page)))  # 下载图片
            except Exception as e:
                # print(e)
                # print("2秒睡眠中")
                time.sleep(2)

if __name__ == '__main__':
    wode = MeiM()
    wode.dio()