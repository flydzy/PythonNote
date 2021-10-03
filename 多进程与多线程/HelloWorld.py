from multiprocessing import Pool
import os

def task(name):
    print("My name is %s" % name)
    return name

def prase_task(res):
    print("You name is %s" % res)

if __name__ == '__main__':
    print("Father Process PID:%s" % os.getpid())
    p= Pool(2)
    for i in range(5):
        p.apply_async(task, args=(i,), callback=prase_task)    
    p.close()
    p.join()
    print('All task done!')