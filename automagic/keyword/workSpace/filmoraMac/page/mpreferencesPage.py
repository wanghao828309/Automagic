#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mhomePage.py
# @Author: wanghao
# @Date  : 2018/11/16


# 【Preferences】窗口-【Performance】
preferences_Performance= ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow[@AXTitle='Preference']/AXGroup/AXCheckBox[@AXTitle='Performance']")

# 【Preferences】窗口-【Performance】-【GPU】
performance_GPU = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow[@AXTitle='Preference']/AXGroup/AXCheckBox[2]")

# 【Preferences】窗口-【Performance】-【proxy】
performance_proxy= ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow[@AXTitle='Preference']/AXGroup/AXCheckBox[0]")

# 【Preferences】窗口-【x】
performance_close = ('xpath',r"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow[@AXTitle='Preference']/AXButton[@AXSubrole='AXCloseButton']")