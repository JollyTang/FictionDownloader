import random

'''
Service层 接收Controller的请求返回相应结果
'''
class Service:
    '''
    初始化函数
    '''
    def __init__(self,mapper):
        self.Mapper = mapper

    '''
    获取任意十本小说
    '''
    def getRandomTenFiction(self):
        index = []
        while True:
            x = random.randint(0, 100)
            if x not in index:
                index.append(x)
            if len(index) == 10:
                break

        res = []
        for i in index:
            res.append(self.Mapper.names[i])

        return res

    '''
    小说查询 
    '''
    def searchFiction(self,str):
        res = []
        for name in self.Mapper.names:
            if str in name:
                res.append(name)

        return res

    '''
    查询全部小说名字
    '''
    def getAllFiction(self):
        return self.Mapper.names

    '''
    下载小说
    '''
    def download(self,name):
        self.Mapper.download(name)