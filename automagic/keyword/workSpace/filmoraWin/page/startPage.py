# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         startPage
# Description:  
# Author:       wanghao
# Date:         2018/10/22
# -------------------------------------------------------------------------------
import sys

if sys.platform.startswith('win'):
    from uiautomation import *


# filmoraWindow = PaneControl(searchDepth=1, ClassName='Qt5QWindowIcon')
class page:
    def __init__(self):
        self.filmoraWindow = PaneControl(searchDepth=1, ClassName='Qt5QWindowIcon')

    # win7的filmora任务栏下标
    def get_filmora9Control(self):
        # ButtonControl(SubName="Wondershare Filmora 9").SetFocus()
        return ButtonControl(searchFromControl=ToolBarControl(Name="运行应用程序"), Name="Wondershare Filmora9")

    # 工程未保存弹出的备份窗口
    def get_backupControl(self):
        return EditControl(searchFromControl=self.filmoraWindow, searchDepth=3)

    # 工程未保存弹出的备份窗口
    def get_backup_no_Control(self):
        return ButtonControl(searchFromControl=self.filmoraWindow, Name="NO")

    # start界面newProject按钮
    def get_newProjectControl(self):
        return ButtonControl(searchFromControl=self.filmoraWindow, searchDepth=2, foundIndex=3)

    # start界面openProject按钮
    def get_openProjectControl(self):
        return ButtonControl(searchFromControl=self.filmoraWindow, searchDepth=2, foundIndex=4)

    # start界面search搜索框
    def get_searchControl(self):
        return EditControl(searchFromControl=self.filmoraWindow, searchDepth=2, foundIndex=1)

    # start界面第n个project library
    def get_proLibraryControl(self, n):
        return ListItemControl(searchFromControl=self.filmoraWindow, foundIndex=n)


if __name__ == '__main__':
    time.sleep(2)
    ButtonControl(Name="Don't Send").Click()
    pass
