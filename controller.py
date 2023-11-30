import art

'''
controller类 用来接受后端传过来的数据并展示给前端
'''
class Controller:
    '''
    构造器
    '''
    def __init__(self,service=None):
        self.service = service
        self.index_1 = 0

    def run(self):
        self.__showpage()
        while True:
            user_input = input()
            if user_input == "1":     # 获取小说列表
                self.__fiction_list_page(self.service.getAllFiction())
            elif user_input == "2":   # 随机推荐10本小说
                print("="*50)
                self.showfiction(self.service.getRandomTenFiction())
                print("=" * 50)
                print("0 回到主界面 2 再推荐10本小说")
            elif user_input == "3":   # 小说搜索
                self.__fiction_list_page(self.search_fiction())
            elif user_input == "4":   # 小说下载
                self.download()
            elif user_input == "5":   # 退出
                print("退出成功")
                break
            elif user_input == "0":
                self.__showpage()
            else:
                print("请重新输入")
                self.__showpage()

    '''
    主页
    '''
    def __showpage(self):
        s = "=" * 100
        print(s)
        art.tprint("fiction downloader")
        print(s)
        print("1 获取小说列表")
        print("2 随机推荐10本小说")
        print("3 小说搜索")
        print("4 小说下载")
        print("5 退出")

    def __fiction_list_page(self,list):
        pagehelper = PageHelper(list)
        while True:
            self.__fiction_list()
            fiction = pagehelper.return_list()
            self.showfiction(fiction)
            print("<- 上一页(h) 下一页(l) -> 退出:q")
            user_input = input()
            if user_input in ["h","l"]:
                pagehelper.change_index(user_input)
            elif user_input == "q":
                print("退出成功")
                self.__showpage()
                break
            else:
                pass

    def __fiction_list(self):
        s = "=" * 50
        print(s)
        art.tprint("fiction list")
        print(s)

    '''
    传来的不是长度为10的数组
    '''
    def showfiction(self,list):
        if len(list) == 10:
            i = 0
            while i < 10:
                print(f"{i + 1}:{list[i]:<50}{i + 2}:{list[i + 1]:<50}")
                i += 2
        else:
            for i in range(len(list)):
                print(f"{i + 1}:{list[i]:<50}",end="")
                if i % 2 != 0:
                    print()

    '''
    下载小说
    '''
    def download(self):
        print("请输入要下载的小说:")
        name = input()
        self.service.download(name)
        print("已下载完全部小说！！！！")
        self.__showpage()
    '''
    小说搜索
    '''
    def search_fiction(self):
        print("请输入关键词:")
        name = input()
        res = self.service.searchFiction(name)
        return res


class PageHelper:
    def __init__(self,list):
        self.__list = list
        self.__index = 0
        self.__length = len(list)
    '''
    返回小说 根据当前Index返回小说 
    '''
    def return_list(self):
        if self.__index + 10 < self.__length:
            return self.__list[self.__index:self.__index + 10]
        else:
            return self.__list[self.__index:]

    def change_index(self,user_input):
        s = "+" * 50
        if user_input == "h":
            if self.__index < 10:
                print(s)
                print("已经是最前面了哦！！")
                print(s)
            else:
                self.__index -= 10
        else:
            if self.__index + 10 > self.__length:
                print(s)
                print("已经是最后面了哦！！")
                print(s)
            else:
                self.__index += 10




