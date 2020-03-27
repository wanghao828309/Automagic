#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
if sys.platform.startswith('win'):
    from uiautomation import *


class page:
    def __init__(self):
        self.paneControl = PaneControl(searchDepth=2, Name='Export')

    # export界面获取【Name】输入框
    def get_NameEditControl(self):
        return EditControl(searchFromControl=self.paneControl, searchDepth=7, foundIndex=1)

    # export界面根据name，获取text的值
    def get_textControl(self, name):
        return TextControl(searchFromControl=self.paneControl, SubName=name)

    # export界面【Resolution】的值
    def get_resolution_textControl(self):
        return TextControl(searchFromControl=self.paneControl, foundIndex=8)

    # export界面【Frame Rate】的值
    def get_frameRate_textControl(self):
        return TextControl(searchFromControl=self.paneControl, foundIndex=10)

    # export界面获取右上角【x】按钮
    def get_closeControl(self):
        self.paneControl.SetFocus()
        return ButtonControl(searchFromControl=self.paneControl)

    # export界面【save to】图标按钮
    def get_saveToControl(self):
        return ButtonControl(searchFromControl=self.paneControl, foundIndex=3)

    # export界面【EXPORT】图标按钮
    def get_exportControl(self):
        return ButtonControl(searchDepth=8, Name='EXPORT', foundIndex=1)

    # export界面，点击【EXPORT】图标按钮，完成后的【CLOSE】按钮
    def get_exportCloseControl(self):
        return ButtonControl(searchDepth=4, Name='CLOSE', foundIndex=1)

    # export界面，点击【EXPORT】图标按钮，完成后的出现的Complete内容
    def get_completedControl(self):
        return TextControl(searchDepth=4, SubName='Completed')

    # export界面，点击【EXPORT】图标按钮，完成后的Elapsed time的内容
    def get_exportElapsedTimeControl(self):
        return TextControl(searchFromControl=self.paneControl, SubName='Elapsed time', foundIndex=1)

    # export窗口【YouTube】界面下，【sign in】弹窗YouTube的title
    def get_YouTube_textControl(self):
        return TextControl(SubName="YouTube Authorization")

    # export窗口【YouTube】界面下，【sign in】弹窗YouTube的【允许】text
    def get_YouTube_allowControl(self):
        return CustomControl(SubName="想要访问", searchDepth=6)

    # export界面【YouTube】界面下，导出完成后的【OK】按钮
    def get_exportYoutobe_okControl(self):
        return ButtonControl(earchFromControl=self.paneControl, Name='OK', foundIndex=1)

    # export界面，获取TextControl通过name
    def get_export_byName_TextControl(self, name):
        return TextControl(earchFromControl=self.paneControl, SubName=name)
