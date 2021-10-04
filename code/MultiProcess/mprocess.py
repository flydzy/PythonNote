from multiprocessing import Process
from os import getpid
from random import randint
from time import time,sleep

def download_task(filename:str)->None:
    print("启动下载进程，进程号[%d]."%getpid())
    print('开始下载%s...' % filename)
    time_to_download = randint(5,10)
    sleep(time_to_download)
    print('%s下载完成！耗费了%d秒' % (filename, time_to_download))

'''装饰器函数'''
def get_time(func):
    def inner(*args, **kwargs):
        start = time()
        result =  func(*args, **kwargs)
        end = time()
        print('总共花费时间为%.2f' % (end - start))
        return result
    return inner

@get_time
def main():
    # start = time()
    p1 = Process(target=download_task, args=('Python入门1.pdf',)) # 创建进程
    p1.start() # 进程启动
    p2 = Process(target=download_task, args=('Python入门2.pdf',))
    p2.start()
    p1.join() # 等待进程结束，如果不加会出现主进程先结束，再结束子进程，此代码不会影响两个进程的执行顺序
    p2.join() 
    # end = time()
    return main.__name__
    

'''
main = get_time(main)
此时的main是inner函数
调用main其实就是调用 inner函数
inner函数会返回func函数的执行结果,可以先针对此函数进行一些操作，然后再将结果返回
'''


if __name__ == '__main__':
    result = main()
    print(result)