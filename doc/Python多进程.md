# Python多进程与多线程

## python多进程

Python的多进程实现有以下两个模块

+ mutilprocessing
  + Process
  + Pool
+ subprocess
其中，`mutilprocessing`模块，主要用于创建属于自身的子进程，而`subprocess`模块，主要用于创建一个独立的，一般不属于自己的子进程，**一般都是用来执行一个外部命令。**

### `mutilprocessing`的Process类实现

#### **方法一:直接创建**

代码如下，直接导入了`Process`类，并通过类的构造函数创建进程，为了实现自定义操作，将自定义操作的函数当作参数传递给`Process`类进程初始化，调用`start()`函数启动进程，将会在`start()`函数的内部，自动调用`run()`函数启动进程。本代码中还提到了一个装饰器函数，主要是用来计算进程的执行时间的，将在以后的文章中介绍。

```python
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
    
if __name__ == '__main__':
    result = main()
    print(result)
```

---

#### **方法二:类继承创建**

代码如下，导入了Process类，自己创建了新类来继承这个类。在初始化函数里面调用Process的`__init__()`函数来进行初始化，紧接着设置`name`属性来标识每一个进程。重写了run函数（**这是必须的**），在run函数中指定自己的操作，本代码指定输出本子进程的名字和进程ID，来标识不同的进程。

`join()`函数是让主进程等待自己的结束，否则出现主进程结束了，子进程还没有运行完，就会成为**孤儿进程**，虽然是**无害**的，但是有时候会不满足我们的要求，所以可以使用`join`函数来让主进程阻塞，来等待子进程结束才执行主进程的相关内容。

> 以下解释是个人思考，需要继续考证。在操作系统上，有同步、异步、阻塞、非阻塞之说，查询资料得知，同步与阻塞，异步与非阻塞是同义词。而当我们启动子进程时，默认是非阻塞的，或者说是异步的，也就是**立即返回结果，而不等待**，这也就会出现，主进程调用启动子进程后，默认是立即返回结果，而不是真正的等待子进程结束，所以就会出现主进程会比子进程先结束。而`join`函数的作用就是，将子进程放到父进程的执行队列中，将异步操作转换为主进程的同步操作，主进程必须等待自己的同步操作（阻塞）情况执行完才能够继续执行。所以`join`翻译过来的意思就是加入主进程,阻塞等待。

```python
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
```

### mutilprocessing的**Pool进程池**实现

前文创建进程时，都是直接使用类来创建，当遇到需要进程比较多的情况时，管理和维护这些进程就会变得很难，因此，有必要使用进程池对进程进行一个管理。进程池的创建很简单，只需要引入Pool对象，就可以直接创建。相关代码如下

```python
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
        # res = p.apply(hard_task, args=(i,)) # 同步调用，阻塞等待结果
        res = p.apply_async(hard_task, args=(i,)) # 异步调用，立刻结束，可以使用get获得返回结果
        res_all.append(res)
    print('Wait for all process done!')
    p.close()
    p.join()
    for res in res_all:
        print(res.get())
    print('All subprocess done!')
```

执行结果为

```shell
2
Parent process 21120.
Run task 0 (21121)
Task 0 runs 2.85 seconds
Run task 1 (21122)
Task 1 runs 0.58 seconds
Run task 2 (21121)
Task 2 runs 1.40 seconds
Run task 3 (21122)
Task 3 runs 2.44 seconds
Wait for all process done!
All subprocess done!
```

> 下面是一些备忘说明，详细的可以参见[这篇博客](https://blog.csdn.net/weixin_44571270/article/details/106577032)

```python
Pool(numprocess,initializer,initargs): # 创建进程池
'numprocess':要创建的进程数，如果省略，将默认使用cpu_count()的值
'initializer'：是每个工作进程启动时要执行的可调用对象，默认为None
'initargs'：是要传给initializer的参数组
```

```python
# 主要方法
p.apply(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。需要强调的是：此操作并不会在所有池工作进程中并执行func函数。如果要通过不同参数并发地执行func函数，必须从不同线程调用p.apply()函数或者使用p.apply_async()

p.apply_async(func [, args [, kwargs]]):在一个池工作进程中执行func(*args,**kwargs),然后返回结果。此方法的结果是AsyncResult类的实例，callback是可调用对象，接收输入参数。当func的结果变为可用时，将理解传递给callback。callback禁止执行任何阻塞操作，否则将接收其他异步操作中的结果。
   
p.close():关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成

P.jion():等待所有工作进程退出。此方法只能在close（）或teminate()之后调用
```
> `apply()`是同步函数，阻塞主进程吗，等待获得结果。返回值就是进程执行的目 标函数的返回结果。`apply_async()`是异步函数，立即执行完毕，不会阻塞主进程，所以主进程可能先执行完毕，此时需要join让主进程等待此进程，可以在返回值使用get()函数获得返回值

> 异步回调函数，指的是在异步操作中，指定一个函数来处理异步操作的结果，而不必等待主进程最后统一处理所有的结果，在创建进程是使用`callback=`属性值即可。

```python
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

# 执行结果
'''
Father Process PID:25901
My name is 0
My name is 1
My name is 2
My name is 3
My name is 4
You name is 0
You name is 2
You name is 3
You name is 4
You name is 1
All task done!
'''
```

可以看到是使用回调函数对进程的执行结果进行了处理。
> `Pool.map()`函数:map()内置函数的并行等价物（尽管它只支持一个可迭代的参数）。它会阻塞，直到结果准备就绪。此方法将iterable内的每一个对象作为单独的任务提交给进程池。可以通过将chunksize设置为正整数来指定这些块的（近似）大小。

```python
# Map函数的用法
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map_async(f, [1, 2, 3]).get()) # 异步不阻塞，与apply_async类似
        print(p.map(f, [1, 2, 3])) # 同步阻塞主进程

# result
# [1, 4, 9]
```

### **进程通信**

每个进程之间是有独立的内存空间的，但是一些场景下，需要让多个进程处理同一个数据，以加快处理速度。因此，也就需要安全有效的进程通信机制。进程通信主要有三种实现方式

+ `Quene`: 队列
+ `Pipe`: 管道
+ `Managers`: 管理器 

> Quene
```python
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
```

两个进程可以无限的执行下去。

> Pipe

```python
from multiprocessing import Process, Pipe
def fun1(conn):
    print('子进程发送消息：')
    conn.send('  你好主进程')
    print('子进程接受消息：')
    print(conn.recv())
    conn.close()

if __name__ == '__main__':
    conn1, conn2 = Pipe() #关键点，pipe实例化生成一个双向管
    p = Process(target=fun1, args=(conn2,)) #conn2传给子进程
    p.start()
    print('主进程接受消息：')
    print(conn1.recv())
    print('主进程发送消息：')
    conn1.send("  你好子进程")
    p.join()
    print('结束测试')

'''
主进程接受消息：
子进程发送消息：
子进程接受消息：
  你好主进程
主进程发送消息：
  你好子进程
结束测试
'''
```

> managers,由 `Manager()` 返回的管理器对象控制一个**服务进程**，该进程保存Python对象并允许其他进程使用代理操作它们。

Manager() 返回的管理器支持类型： list 、 dict 、 Namespace 、 Lock 、 RLock 、 Semaphore 、 BoundedSemaphore 、 Condition 、 Event 、 Barrier 、 Queue 、 Value 和 Array 

```python
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
```
> 一些参考资料

[1 官方文档](https://docs.python.org/zh-cn/3/library/multiprocessing.html)

[2 博客](https://blog.csdn.net/weixin_44571270/article/details/106577032)

[3 廖雪峰博客](https://www.liaoxuefeng.com/wiki/1016959663602400/1017628290184064#0)

---

### `subprocess`模块实现

`subprocess`模块可以生成新的进程，连接到它们的input/output/error管道，同时获取它们的返回码。本文只做一些基本操作的介绍，详细的请看[这篇文章](https://www.jianshu.com/p/430c411160f8)，十分详细。

subprocess的基本对象的`Popen`，subprocess的大部分功能都是基于此对象实现的。此对象的构造函数有许多的参数，分别是

+ `args`:需要执行的命令，默认是列表或者元组
+ `shell`:默认是False，当为True时，上述参数可以为字符串
+ `stdout,stdin,stderr`:三大标准流，不指定则为`None`,可以指定为`subprocess.PIPE`、文件描述符、文件对象。若指定为`subpprocess.PIPE`,则表示将创建新的管道，使用Popen对象的方法进行读写。若是`None`，则会继承父进程的输入输出方法。
+ `universal_newlines`:不同系统的换行符不同。若True，则该文件对象的stdin，stdout和stderr将会以文本流方式打开；否则以二进制流方式打开。

使用`subprocess`可以分为两个方面，可以直接简单化的，基于Popen对象实现的函数。

1. `run()`函数:返回值为CompletedProcess类；其中包含有args和returncode（0：成功|1：失败），若指定了stdout，则包含stdout。
2. `call()`函数：执行args命令，返回值为命令执行状态码；若无stdout,则输出到标准输出流。
3. `check_call()`函数：与call相同，只是失败会抛出异常
4. `check_output()`函数：成功会返回命令输出结果，失败会抛出异常

```python
def otherFunction():
    '''都是封装好的，基于Popen对象实现的函数，可以直接调用而不用事先创建对象'''
    subprocess.run(args[, stdout, stderr, shell ...]) 
    subprocess.call(args[, stdout, ...])
    subprocess.check_call(args[, stdout, ...])
    subprocess.check_output(args[, stderr, ...])
```

简单的函数封装使用起来简单，但是灵活度不高，追求更高的灵活读，可以使用`Popen`对象来创建相应的对象，执行命令。相关的代码如下：

```python
# 使用Popen对象来创建新的进程

import subprocess
from sys import stderr, stdin, stdout

def createSubProcess():
    # 不指定任何的输入输出流，那么将会默认的将输入输出定义为系统的标准输入输出流
    process1 = subprocess.Popen(['nslookup','www.baidu.com']) # 直接创建进程执行外部命令，以列表或元组的形式
    process2 = subprocess.Popen('nslookup www.baidu.com', shell=True) # 直接创建进程执行外部命令，以字符串的形式
    print(process1)
    print(process2)

# 给进程指定输入流，可以通过函数调用的方法进行输入，会以系统默认的标准输出为输出
def subProcessWithStdin():
    process = subprocess.Popen(['python3'],stdin=subprocess.PIPE, encoding='utf-8')
    process.stdin.write('print("hello world")')  # 输出：hello world
    process.stdin.close()
    print(process) # 结果是一个对象 <Popen: returncode: None args: ['python3']>

'''
<Popen: returncode: None args: ['python3']>
[root@VM-4-12-centos python]# hello world
可以看到，是先执行了最后面的print函数，后输出的hello world，表示此操作是异步的，主进程先执行完再执行子进程的
'''

# 给进程指定输出流，可以通过函数调用的方法获得输出，不会在系统默认的标准暑促进行输出
def subProcessWithStdOut():
    process = subprocess.Popen(['nslookup', 'www.baidu.com'], stdout=subprocess.PIPE)
    result = process.stdout.readlines()
    process.stdout.close()
    print(result) # [b'Server:\t\t183.60.83.19\n', b'Address:\t183.60.83.19#53\n', b'\n', b'Non-authoritative answer:\n', b'www.baidu.com\tcanonical name = www.a.shifen.com.\n', b'Name:\twww.a.shifen.com\n', b'Address: 112.80.248.75\n', b'Name:\twww.a.shifen.com\n', b'Address: 112.80.248.76\n', b'\n'][b'Server:\t\t183.60.83.19\n', b'Address:\t183.60.83.19#53\n', b'\n', b'Non-authoritative answer:\n', b'www.baidu.com\tcanonical name = www.a.shifen.com.\n', b'Name:\twww.a.shifen.com\n', b'Address: 112.80.248.75\n', b'Name:\twww.a.shifen.com\n', b'Address: 112.80.248.76\n', b'\n']

# 同时指定输入输出流, 那么将会以指定的输入输出流进行输入输出
def subProcessWithInAndOut():
    process = subprocess.Popen(['python3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    process.stdin.write("print('hello world')")
    process.stdin.close()
    result = process.stdout.read()
    process.stdout.close()
    print(result) # hello world

# 指定输入输出流和错误流
def subProcessWithInOutErr():
    args = ["python3", "python1"]
    for arg in args:
        process = subprocess.Popen(arg, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        process.stdin.write("print('Hello World')")
        process.stdin.close()
        out = process.stdout.read()
        process.stdout.close()
        err = process.stderr.read()
        print('out:%s, err:%s' % (out, err)) 
        # 第一个结果：out:Hello World, err:
        # 第二个结果：FileNotFoundError: [Errno 2] No such file or directory: 'python1'

# communicate(([input, timeout])函数与子进程交互,如果指定input内容，是将input内容输入到stdin流中
# 返回值为一个元组，(stdout, stderr),会阻塞父进程直到结束
def subProcessWithCommunicate():
    process = subprocess.Popen("python3", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate("print('Hello World')")
    print(stdout, stderr) # Hello World
    process2 = subprocess.Popen("python3", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    stdout2, stderr2 = process2.communicate("noprint('Hello World')")
    print(stdout2, stderr2) #  NameError: name 'noprint' is not defined

# popen对象的其他函数
def objectFunction():
    process = subprocess.Popen('nslookup www.baidu.com')
    process.poll() # 用于检查命令是否已经执行结束，若结束返回状态码；若未结束返回None；
    process.wait() # 等待子进程结束，并返回状态码；若超过timeout(s)进程仍未结束，则抛出异常；
    process.send_signal() # 发送信号signal给子进程；
    process.terminate() # 停止子进程；
    process.kill() # 杀死子进程

if __name__ == '__main__':
    # createSubProcess()
    # subProcessWithStdin()
    # subProcessWithStdOut()
    # subProcessWithInAndOut()
    # subProcessWithInOutErr()
    # subProcessWithCommunicate()
```

关于此对象的介绍就到这里，详细的了解和使用还是需要到实战中。