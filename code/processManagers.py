# managers 实现线程通信
from multiprocessing import Manager, Process, process
import time

def plus_one_task(num):
    while True:
        num.value = num.value + 1
        print("plus one reslut %d" % num.value)
        time.sleep(2)

def minus_two_task(value):
    while True:
        num.value = num.value - 2
        print('minus two result %d' % num.value)
        time.sleep(2)
if __name__ == '__main__':
    with Manager() as maneger:
        num = maneger.Value('i',1)
        p_plusone = Process(target = plus_one_task, args=(num,))
        p_minustwo = Process(target = minus_two_task, args=(num,))
        p_plusone.start()
        p_minustwo.start()
        p_minustwo.join()
        p_plusone.join()

'''
plus one reslut 2
minus two result 0
plus one reslut -2
minus two result -2
minus two result -4
plus one reslut -3
plus one reslut -2
minus two result -4
plus one reslut -6
minus two result -6
plus one reslut -8
'''
