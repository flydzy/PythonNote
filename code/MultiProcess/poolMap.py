# Map函数的用法
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map_async(f, [1, 2, 3]).get()) # 异步不阻塞
        print(p.map(f, [1, 2, 3])) # 同步阻塞主进程