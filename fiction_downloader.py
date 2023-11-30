from service import Service
from controller import Controller
from mapper import Mapper

class fiction_downloader():
    def __init__(self):
        mapper = Mapper()
        service = Service(mapper)
        self.controller = Controller(service)

    def run(self):
        self.controller.run()


if __name__ == '__main__':
    fiction_downloader().run()
