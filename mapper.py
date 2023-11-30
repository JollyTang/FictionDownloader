import asyncio
import os
import aiofiles
import aiohttp
import requests
from lxml import etree


def rename(oldtitle):
    title = ""
    for i in oldtitle:
        title += i
    title = title.replace("/", "").replace("*","").replace("?","")
    return title



async def get_next_url(url,headers,fictname):
    print("start getting next url")
    requests.packages.urllib3.disable_warnings()
    responce = requests.get(url,headers=headers)
    responce.encoding = 'gbk'
    href = etree.HTML(responce.text).xpath('//*[@id="list"]/dl/dd[position() >= 1]/a/@href')
    title = etree.HTML(responce.text).xpath('//*[@id="list"]/dl/dd[position() >= 1]/a/text()')
    task = []
    print("already get all url and title")
    for t in range(len(href)):
        print("old = ",title[t])
        newtitle = rename(title[t])
        print("new = ",newtitle)
        nexturl = url.rsplit('/',1)[0] + href[t]
        print(f"now process {nexturl} and its title is {newtitle}")
        task.append(asyncio.create_task(get_fiction(nexturl,headers,newtitle,fictname)))
        print(f"create task {newtitle} over!!!")

    await asyncio.wait(task)





async def get_fiction(url,headers,title,fictname):


    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url,headers=headers,ssl=False) as resp:
            print(f'{title}',resp.status)
            str = await resp.text(encoding='gb18030')
            content = etree.HTML(str).xpath('//*[@id="content"]/text()')
            text = ""
            for s in content:
                s.replace(f'\u3000','')
                text += s
                text += '\n'
            async with aiofiles.open(f'../{fictname}小说/{title}.txt',mode='w',encoding='utf-8') as f:
                await f.write(text)

        print(f'已下载完{title}')

def getfict(fict,fictname):
    if not os.path.exists(f"../{fictname}小说"):
        os.mkdir(f"../{fictname}小说")
    url = fict
    # url = f'https://www.ddyueshu.com/{fict}'
    print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"
    }
    print("start running")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_next_url(url, headers,fictname))


'''
伪持久层 
'''
class Mapper:
    '''
    初始化函数，初始化过程中自动获取所有小说列表 包括小说名字以及小说url
    '''
    def __init__(self):
        self.hrefs,self.names,self.library = self.__getAllFictionName()


    '''
    爬取所有小说名字和url 存储起来
    '''
    def __getAllFictionName(self):
        proxies = {"http": None, "https": None}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
        }
        r = requests.get("https://www.ddyueshu.com/xiaoshuodaquan/", proxies=proxies, headers=headers)
        hrefs = etree.HTML(r.text).xpath("//*[@id='main']/div[1]/ul/li[position() >= 0]/a/@href")
        names = etree.HTML(r.text).xpath("//*[@id='main']/div[1]/ul/li[position() >= 0]/a/text()")
        d = dict(zip(names,hrefs))
        return (hrefs,names,d)

    '''
    下载小说
    '''
    def download(self,name):
        if(name not in self.names):
            print("没有该小说")
            return
        u = ""
        for i in self.library[name]:
            u += i
        u = u[:-1]
        print(u)
        getfict(u,name)

