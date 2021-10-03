# 多进程类继承方法实现
from multiprocessing import Process
import os, time
import random

class MyMutilProcess(Process):
    
    def __init__(self, name):
        super(MyMutilProcess, self).__init__()
        self.name = name
    
    # 重写run函数，实现在多进程里面的自定义操作
    def run(self) -> None:
        time.sleep(random.randint(3,5)) # 阻塞3到5秒
        print('我是进程%s (%s)' % (self.name, os.getpid()))

if __name__ == '__main__':
    print('我是主进程(%s)' % os.getpid())
    process1 = MyMutilProcess("process1") # 创建进程1
    process1.start() # 启动进程，会在内部自动调用run函数
    process1.join() # 主进程等待进程1结束

    process2 = MyMutilProcess("process2")
    process2.start()
    process2.join() # 主进程等到进程2结束，才会结束

    print("所有的进程都执行完了")