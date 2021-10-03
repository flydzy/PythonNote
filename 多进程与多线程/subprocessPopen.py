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

def objectFunction():
    process = subprocess.Popen('nslookup www.baidu.com')
    process.poll() # 用于检查命令是否已经执行结束，若结束返回状态码；若未结束返回None；
    process.wait() # 等待子进程结束，并返回状态码；若超过timeout(s)进程仍未结束，则抛出异常；
    process.send_signal() # 发送信号signal给子进程；
    process.terminate() # 停止子进程；
    process.kill() # 杀死子进程

def otherFunction():
    '''都是封装好的，基于Popen对象实现的函数，可以直接调用而不用事先创建对象'''
    subprocess.run(args[, stdout, stderr, shell ...]) 
    subprocess.call(args[, stdout, ...])
    subprocess.check_call(args[, stdout, ...])
    subprocess.check_output(args[, stderr, ...])

if __name__ == '__main__':
    # createSubProcess()
    # subProcessWithStdin()
    # subProcessWithStdOut()
    # subProcessWithInAndOut()
    # subProcessWithInOutErr()
    # subProcessWithCommunicate()