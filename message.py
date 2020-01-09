#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import threading
#import sys
import inspect
import ctypes
#import os


#server端：
#import socket
#sk = socket.socket()
#sk.bind(('127.0.0.1',8898))  #把地址绑定到套接字
#sk.listen()          #监听链接
#conn,addr = sk.accept() #接受客户端链接
#ret = conn.recv(1024)  #接收客户端信息
#print(ret)       #打印客户端信息
#conn.send(b'hi')        #向客户端发送信息
#conn.close()       #关闭客户端套接字
#sk.close()        #关闭服务器套接字(可选)

a = 1
sk = socket.socket()           # 创建客户套接字
sk.connect(('127.0.0.1',9999))    # 尝试连接服务器
sk.send(b':n 8089d')

#停止线程，我也不知道到底有用没用
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    
#引用方法 stop_thread(myThread)


#把接收放到进程里面去，就可以持续接收server的信息了。
class recvthread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        
    def run(self):
        print ("数据接收线程就绪：" + self.name)
        while True:
            ret = sk.recv(1024)         # 对话(发送/接收)
            #判断是空字节就跳出，否则要死循环
            str = ret.decode()
            if str=='':
                
                print("请随便输入字符按ENTER后退出... \r\n")
                break
                

            print(str+"\r\n---------------")
            
            
        #print ("退出线程：" + self.name)

class sendthread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        
    def run(self):
        print ("文字输入线程就绪：" + self.name)
        while a == 1:
            #print("请输入：")
            str = input() #s要转换为字节了才能发送
            #输入:q表示退出
            if str == ":q":
                stop_thread(thread1)
                sk.close()
                exit()
                
            if str == ":h": #帮助
                print(":q 退出 :l 显示客户 :n 改名 :t 私信")
                str = ""
            
            if a == 0:
                #print(a)
                break
            sk.send(str.encode())
            print("---------------") #\r\n

        #print ("退出线程：" + self.name)


thread1 = recvthread(1)
thread2 = sendthread(2)
thread1.start()
thread2.start()

print("------------------------------------")
print("-欢迎使用信息发送系统1.0 版权：黄浩-")
print("------------------------------------")
print(":q 退出 :l 显示客户 :n 改名 :t 私信")
print("------------------------------------")


thread1.join()
a = 0
#sys.exit(1)
#os._exit(0)
#stop_thread(thread2)
#thread2.terminate()

thread2.join()
sk.close() 
print ("客户端退出")
           # 关闭客户套接字
           
exit()
