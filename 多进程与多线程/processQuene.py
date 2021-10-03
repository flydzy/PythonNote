# 使用队列Quene进行进程通信

from multiprocessing import Pool, Queue
from multiprocessing.context import Process
import os, time
import queue


# 向队列中放数据
def put_task(quene):
    while True:
        print("我是放置数据的任务，我正在写入数据")
        quene.put('我放数据咯')
        time.sleep(2)

def get_task(quene):
    while True:
        result = quene.get()
        print('获取结果:%s' % result)
        time.sleep(3)

if __name__ == '__main__':
    quene = Queue()
    putprocess = Process(target=put_task, args=(quene,))
    getprocess = Process(target=get_task, args=(quene,))
    putprocess.start()
    getprocess.start()
    putprocess.join()
    getprocess.join()

'''运行结果
我是放置数据的任务，我正在写入数据
获取结果:我放数据咯
我是放置数据的任务，我正在写入数据
获取结果:我放数据咯
我是放置数据的任务，我正在写入数据
我是放置数据的任务，我正在写入数据
获取结果:我放数据咯
我是放置数据的任务，我正在写入数据
获取结果:我放数据咯
我是放置数据的任务，我正在写入数据
我是放置数据的任务，我正在写入数据
获取结果:我放数据咯

'''