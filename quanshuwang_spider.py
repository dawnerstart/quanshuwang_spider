import requests,re,time
#1、获取斗罗大陆html，解码存入book，正则匹配各章连接和章名，存入该chapters
#2、对每一个章节，解码存入chapter，正则匹配正文，存入该txt，txt叫章名
html=r'http://www.quanshuwang.com/book/44/44683'
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
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
        xiaoshuo1=xiaoshuo1.replace('&nbsp;&nbsp;&nbsp;&nbsp;','').replace('<br />','')
        print(xiaoshuo1)
        with open('.\quanshuwang\%s.txt'%(chapter[1]),'w') as f:
            f.write(xiaoshuo1)
        #time.sleep(10)
