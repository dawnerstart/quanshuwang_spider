'''
Author: your name
Date: 2021-04-05 20:37:58
LastEditTime: 2021-04-06 00:33:44
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Python\爬虫\test.py
'''
import requests,re,time
#1、获取斗罗大陆html，解码存入book，正则匹配各章连接和章名，存入该chapters
#2、对每一个章节，解码存入chapter，正则匹配正文，存入该txt，txt叫章名
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}
for classes in range(1,12):
    class_html='http://www.quanshuwang.com/list/'+str(classes)+'_1.html'
    print(class_html)
    class_html_o=requests.get(class_html,headers=header).content.decode('gbk')
    #print(class_html_o)
    class_html_reg=re.compile(r'<a href=".*?" class="last">(.*?)</a>',re.S)
    pagemax=class_html_reg.findall(class_html_o)
    #print(pagemax)
    for page in range(1,int(pagemax[0])+1):
        page_html='http://www.quanshuwang.com/list/'+str(classes)+'_'+str(page)+'.html'
        page_html_o=requests.get(page_html,headers=header).content.decode('gbk')
        page_html_reg=r'</a></em><a href="(.*?)" class="readTo">马上阅读</a></span></li>'
        page_html_reg=re.compile(page_html_reg,re.S);
        literatures=page_html_reg.findall(page_html_o)
        #print(literatures)
        #print('````````````````````')
        for literature in literatures:
            literature_html=str(literature)
            #print('`````````````````````````````')
            literature_html_o=requests.get(literature_html,headers=header).content.decode('gbk')
            #print(literature_html_o)
            literature_html_reg=r'<div class="b-oper">.*?<a href="(.*?)" class="reader" title=.*?开始阅读</a>'
            literature_html_reg=re.compile(literature_html_reg,re.S)
            link=literature_html_reg.findall(literature_html_o)
            html=str(link[0])
            book=requests.get(html,headers=header).content.decode('gbk')   #书源码
            book_regular=r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'   #书正则
            book_regular=re.compile(book_regular)
            chapters=re.findall(book_regular,book)  #各章节
            for chapter in chapters:
                content=requests.get(chapter[0],headers=header).content.decode('gbk')
                content_regular=r'</script>&nbsp;&nbsp;&nbsp;&nbsp;.*?<br />(.*?)<script type="text/javascript">'
                content_regular=re.compile(content_regular,re.S)
                xiaoshuo=content_regular.findall(content)
                for xiaoshuo1 in xiaoshuo:
                    name=re.sub('[\/:*?"<>|， ./_-]','',chapter[1])
                    xiaoshuo1=xiaoshuo1.replace('&nbsp;&nbsp;&nbsp;&nbsp;','').replace('<br />','')
                    print('写文件'+str(name))
                    with open('.\quanshuwang\%s.txt'%(str(name)),'w') as f:
                        f.write(xiaoshuo1)
                    time.sleep(3)
