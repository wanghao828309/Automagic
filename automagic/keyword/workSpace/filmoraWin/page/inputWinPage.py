# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         inputWinPage
# Description:  
# Author:       wanghao
# Date:         2018/10/22
# -------------------------------------------------------------------------------
import sys
if sys.platform.startswith('win'):
    from uiautomation import *

class page:
    def __init__(self):
        self.floderControl = PaneControl(ClassName='DUIListView', searchDepth=7)
        self.winControl = WindowControl(Name="resource")

    # input窗口地址栏输入框
    def get_hostControl(self):
        progressBarControl = ProgressBarControl(ClassName="msctls_progress32", searchDepth=6, foundIndex=1)
        return  ToolBarControl(searchFromControl=progressBarControl, foundIndex=1)

    # input窗口文件夹视图
    def get_floderControl(self):
        return ListControl(ClassName='UIItemsView')

    # input窗口文件夹视图下的第num文件
    def get_fileControl(self,num):
        return ListItemControl(searchFromControl=self.floderControl, foundIndex=int(num))

    # input窗口文件夹视图下的具体文件夹
    def get_floderControl_by_name(self,name):
        openProjectControl = ListItemControl(searchFromControl=self.floderControl, SubName=name)
        return openProjectControl

    # input窗口右下角打开按钮
    def get_openControl(self):
        filmoraControl = PaneControl(Name="Wondershare Filmora 9", searchDepth=1)
        return ButtonControl(searchFromControl=filmoraControl, Name="打开(O)", searchDepth=3)

    # win窗口右上角【最大化/缩小】按钮
    def get_minOrMaxControl(self):
        return ButtonControl(searchFromControl=self.winControl, searchDepth=3, foundIndex=2)

    # win窗口右上角【最大化】按钮
    def get_maxControl(self):
        return ButtonControl(searchFromControl=self.winControl, Name="最大化")

    # win窗口右上角【最小化】按钮
    def get_minControl(self):
        return ButtonControl(searchFromControl=self.winControl, searchDepth=3, foundIndex=1)

    # win窗口【Import a Media Folder】的计算机选项
    def get_folderComputerControl(self,name):
        return TreeItemControl(Name=name, foundIndex=1)

    # win窗口【Import a Media Folder】的确定按钮
    def get_folderSureControl(self):
        return ButtonControl(Name="确定", searchDepth=3)

    # export窗口，点击【save to】图标按钮，弹出win窗口地址输入框
    def get_export_hostControl(self):
        return ToolBarControl(ClassName="ToolbarWindow32", foundIndex=2)

    # export窗口，点击【save to】图标按钮，弹出win窗口【选择文件夹】按钮
    def get_export_selectFloderControl(self):
        return ButtonControl(Name="选择文件夹", foundIndex=1)

if __name__ == '__main__':
    pass
