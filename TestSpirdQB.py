#-*- coding:utf-8 -*-

import urllib2
import re
#糗百爬虫类
class QSBK:
    #初始化方法，定义了一些变量
    def __init__(self):
        self.pageIndex = 1
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #headers
        self.headers = {'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'}
        #程序是否继续运行的变量
        self.enable = False

    def getPage(self,pageIndex):
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            req = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(req,timeout=10)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"code"):
                print "链接糗百失败，错误码:",e.code
            if hasattr(e,"reason"):
                print "链接糗百失败，错误原因:",e.reason

    #获得传入页的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load file..."
            return None
        pattern = re.compile(r'<div class="author clearfix".*?title="(.*?)">.*?<span>(.*?)</span>.*?'+
                             r'<div class="stats">.*?class="number">(.*?)</i>.*?class="qiushi_comments".*? class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子们
        pageStories = []
        patternitem1 = re.compile(r'<br/>')
        for item in items:
            text = re.sub(patternitem1,"\n",item[1])
            pageStories.append([(item[0]).strip(),text.strip(),item[2].strip(),(item[3]).strip()])
        return pageStories

    #加载并提取页面的内容，导入到stories中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories)<2:
                #get a new page
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #该方法的作用是每页敲回车只打印一个段子的内容
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q" or input =="q":
                self.enable =False
                return
            print "第%d页\t发布人:%s\t赞:%s\t评论:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    #开始方法
    def start(self):
        print "正在读取糗百，按回车查看内容，Q/q退出"
        #设置变量为True，可以正常读取
        self.enable = True
        #加载一页内容
        self.loadPage()
        #局部变量，控制当前督导第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前页加1
                nowPage += 1
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)

if __name__== "__main__":
    spider = QSBK()
    spider.start()