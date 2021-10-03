from multiprocessing import Pool
import os, random, time

# 进程需要执行的任务
def hard_task(name):
    print('Run task %s (%s)' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    # print('Task %s runs %0.2f seconds' % (name, (end-start)))
    return 'Task %s runs %0.2f seconds' % (name, (end-start))
    
# 在 __main__ 下面创建进程，保护程序的入口
if __name__ == '__main__':
    print(os.cpu_count())
    print('Parent process %s.' % os.getpid())
    p = Pool()
    res_all = []
    for i in range(4):
        # res = p.apply(hard_task, args=(i,)) # 1. 同步调用，阻塞等待结果
        res = p.apply_async(hard_task, args=(i,)) # 2. 异步调用，立刻结束，可以使用get获得返回结果
        res_all.append(res)
    print('Wait for all process done!')
    p.close()
    p.join()
    for res in res_all:
        print(res.get())
    print('All subprocess done!')