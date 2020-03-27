#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mhomePage.py
# @Author: wanghao
# @Date  : 2018/11/16


# 窗口关闭按钮
close_button = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow/AXButton[@AXSubrole='AXCloseButton']")

# home窗口-登录头像
user_login = ('id', r"_NS:220")

# home窗口-登录头像-【login】
login_continue_button = ('id','_NS:66')

# 用户输入用户名，密码点击登录后加载的窗口
loading_state = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow/AXScrollArea/AXWebArea")

# 用户登录成功窗口--【state】内容，例如：Lifetime Plan
user_state = ('id', r"_NS:57")

# home窗口-左上角【file】选项
file_select = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXMenuBar/AXMenuBarItem[@AXTitle='File']")

# home窗口-【file】-【Project Setting】
file_proSetting= ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXMenuBar/AXMenuBarItem[@AXTitle='File']/AXMenu/AXMenuItem[@AXTitle='Project Setting']")

# home窗口-左上角【Wondershare Filmora 9】选项
filmora9_select = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9'/AXMenuBar/AXMenuBarItem[@AXTitle='Wondershare Filmora 9']")

# home窗口-【Wondershare Filmora 9】-【Preferences】
filmora9_Preferences = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9'/AXMenuBar/AXMenuBarItem[@AXTitle='Wondershare Filmora 9']/AXMenu/AXMenuItem[@AXTitle='Preferences…']")
