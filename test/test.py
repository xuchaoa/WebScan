import multiprocessing
import os
import time

def run_task(name):
    print('Task {0} pid {1} is running'.format(name, os.getpid()))
    time.sleep(1)
    print('Task {0} end.'.format(name))

if __name__ == '__main__':
    print('current process {0}'.format(os.getpid()))
    p = multiprocessing.Pool(processes=3)  #设置进程池并发最大数量
    for i in range(6):
        p.apply_async(run_task, args=(i,))
    # for循环改为这个一样的效果      p.map(run_task,[i for i in range(6)])
    print('Waiting for all subprocesses done...')
    p.close() #关闭进程池，不允许新进程进入
    p.join()  #主进程阻塞，等待其他进程执行完成
    print('All processes done!')  #主进程结束