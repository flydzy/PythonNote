'''子进程并不是自身，而是一个外部进程，除了创建以外，还要控制子进程的输入输出'''

import subprocess

# 直接执行相关外部命令创建子进程

# 使用call调用创建进程执行命令，返回值是命令执行状态码
# 若执行成功，则函数返回值为0；若执行失败，则函数返回值为1；
print('nslookup www.python.org')
process_call = subprocess.call(['nslookup','www.python.org'])
print("Exit code:", process_call)

# 使用run调用创建进程执行命令，返回值是CompletedProcess
# 函数返回值CompletedProcess中包含有args和returncode
process_run = subprocess.run(['nslookup','www.baidu.com'])
print(process_run.returncode)

# 上述还有check_call()函数和check_output()函数，
# 前者返回执行状态码或异常，后者返回执行结果或异常

# 子进程输入
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print("Exit code:", p.returncode)