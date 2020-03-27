#!C:/Python27
# coding=utf-8

from ctypes import *
import os
import sys
import ftplib


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host, port='21'):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print self.ftp.welcome

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        print  file_handler
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 接收服务器上文件并写入本地文件
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)  # 上传文件
        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False
        print "LocalDir:", LocalDir
        LocalNames = os.listdir(LocalDir)
        print "list:", LocalNames
        print RemoteDir
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print "remoteDir:", RemoteDir
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print "RemoteNames", RemoteNames
        print self.ftp.nlst("/del1")
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    filename = "/Users/ws/Documents/filmora9.0_AutoMagic/keyword/result/2018-11-14/2018-11-14-19_18_29_result.html"

    #拷贝文件到服务器
    try:
        ftp = myFtp('192.168.11.83')
        ftp.Login('wanghao', '123456')  # 登录，如果匿名登录则用空串代替即可
        print filename
        if sys.platform.startswith('win'):
            fileList = filename.split("\\")
        else:
            fileList = filename.split("/")
        print 'fileList： /home/wanghao/report/'+fileList[-1]
        ftp.UpLoadFile(filename,'/home/wanghao/report/html/'+fileList[-1])
        ftp.close()
    except Exception as err:
        print "Html报告上传到服务器失败:"+err.message
