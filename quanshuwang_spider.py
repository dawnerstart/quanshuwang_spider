import requests,re,os,time
#1、获取斗罗大陆html，解码存入book，正则匹配各章连接和章名，存入该chapters
#2、对每一个章节，解码存入chapter，正则匹配正文，存入该txt，txt叫章名
x=1
def classdir(str1:str):
    path=str1
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

header={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
for classes in range(9,12):  #遍历每个类
    class_html='http://www.quanshuwang.com/list/'+str(classes)+'_1.html'
    ##################print(class_html)
    class_html_o=requests.get(class_html,headers=header).content.decode('gbk')
    time.sleep(2);
    class_html_reg=re.compile(r'<a href=".*?" class="last">(.*?)</a>',re.S)
    pagemax=class_html_reg.findall(class_html_o)    #得到每个类的最大页
    
    pagemax=int(pagemax[0])
    classdir_reg=re.compile(r'<title>(.*?)_全书网</title>')
    classdir_name=classdir_reg.findall(class_html_o)
    print(pagemax)

    if classdir_name==[]:
        classdir_name=str(x)
        x+=1
    else:
        classdir_name=classdir_name[0]
    #bookpath='./quanshuwang/'+classdir_name+'/' #+bookdir_name+'/'
    #classdir(bookpath)  #创建类
    for page in range(1,pagemax+1): #遍历每个类的每一页
        page_html='http://www.quanshuwang.com/list/'+str(classes)+'_'+str(page)+'.html'
        page_html_o=requests.get(page_html,headers=header).content.decode('gbk')
        time.sleep(2);
        page_html_reg=r'</a></em><a href="(.*?)" class="readTo">马上阅读</a></span></li>'
        page_html_reg=re.compile(page_html_reg,re.S);
        literatures=page_html_reg.findall(page_html_o)  #得到每一页的“马上阅读”连接
        if literatures!=[]:
            for literature in literatures:  #遍历每个“马上阅读”连接
                literature_html_o=requests.get(literature,headers=header).content.decode('gbk')
                time.sleep(2);
                literature_html_reg=r'<div class="b-oper">.*?<a href="(.*?)" class="reader" title=.*?开始阅读</a>'
                bookname_reg=r'<meta property="og:title" content="(.*?)"/>'
                literature_html_reg=re.compile(literature_html_reg,re.S)
                bookname_reg=re.compile(bookname_reg,re.S)
                link=literature_html_reg.findall(literature_html_o) #得到“开始阅读”连接
                book_dir_name=bookname_reg.findall(literature_html_o)   #书的目录名
                if book_dir_name==[]:
                    book_dir_name=str(x)
                    x+=1
                else:
                    book_dir_name=book_dir_name[0]
                bookpath='./quanshuwang/'+classdir_name+'/'
                bookpath=bookpath+book_dir_name+'/'
                os.makedirs(bookpath)



                
                print(link)
                if link!=[]:    #若“开始阅读”连接存在
                    html=str(link[0])
                    book=requests.get(html,headers=header).content.decode('gbk')   #书源码
                    time.sleep(2);
                    book_regular=r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'   #书正则
                    book_regular=re.compile(book_regular)
                    chapters=re.findall(book_regular,book)  #各章节连接
                    #bookpath='./quanshuwang/'+classdir_name+'/' #+bookdir_name+'/'
                    #classdir(bookpath)
                    for chapter in chapters:    #对每个章节
                        content=requests.get(chapter[0],headers=header).content.decode('gbk')
                        time.sleep(2);
                        content_regular=r'</script>&nbsp;&nbsp;&nbsp;&nbsp;.*?<br />(.*?)<script type="text/javascript">'
                        content_regular=re.compile(content_regular,re.S)
                        xiaoshuo=content_regular.findall(content)
                        for xiaoshuo1 in xiaoshuo:
                            name=re.sub('[\/:*?"<>|， ./_-]','',chapter[1])
                            xiaoshuo1=xiaoshuo1.replace('&nbsp;&nbsp;&nbsp;&nbsp;','').replace('<br />','')
                            print('写文件'+str(name))
                            
                            print(bookpath)
                            #bookpath=bookpath+book_dir_name+'/'
                            with open(bookpath+'/%s.txt'%(name),'w') as f:
                                f.write(xiaoshuo1)
                        time.sleep(3);
                    #time.sleep(6)
                else:
                    time.sleep(6)
                    # continue
                    #time.sleep(1)
