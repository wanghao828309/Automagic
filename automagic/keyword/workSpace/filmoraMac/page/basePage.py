# -*- coding: utf-8 -*-

import time, datetime
import os, sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import paramiko
import re




# 获取系统当前时间
def saveTime():
    """
    返回当前系统时间以括号中（2014-08-29-15_21_55）展示
    """
    return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))


"""
下面的方法针对selenium的web自动化
"""

# 元素高亮显示
def highlightElement(self, element):
    self.driver.execute_script("element = arguments[0];" +
                               "original_style = element.getAttribute('style');" +
                               "element.setAttribute('style', original_style + \";" +
                               "background: #1874cd; border: 2px solid red;\");" +
                               "setTimeout(function(){element.setAttribute('style', original_style);}, 1000);",
                               element)

# 页面顶部加步骤输出
def notes(self, text):
    js1 = u"""var bodyDom = document.getElementsByTagName('body')[0];
            var insertDiv = document.createElement('div');
            insertDiv.id = 'sdiv';
            insertDiv.style.backgroundColor = 'red';
            insertDiv.style.height = '20px';
            insertDiv.style.color = '#FFF';
            insertDiv.style.textalign = 'center';
            insertDiv.innerText = '"""
    js2 = u"""';
            var firstdiv = bodyDom.getElementsByTagName('div')[0];
            bodyDom.insertBefore(insertDiv,firstdiv);
            """
    js = js1 + text + js2
    self.driver.execute_script(js)

# 更新顶部note显示内容
def show_note(self, stext):
    js = u"insertDiv = document.getElementById('sdiv');insertDiv.innerText ='" + stext + "';"
    self.save_runing_log(stext)
    self.driver.execute_script(js)

# 重写定义send_keys方法
def send_keys(self, loc, value):
    try:
        self.find_element(loc).clear()
    except:
        print u"%s 元素 %s 没有clear属性" % (self, loc)
    self.find_element(loc).send_keys(value)

# 重写元素定位方法
def find_element(self, loc):
    for i in xrange(3):
        try:
            # WebDriverWait(self.driver, 15).until(lambda driver: True if driver.find_element(*loc) is not None else False)
            element = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc))
            # element = self.driver.find_element(*loc)
            # self.highlightElement(element)
            return element
        except:
            pass
    # print u"%s 页面中未能找到 %s 元素" % (self, loc)

# 重写一组元素定位方法
def find_elements(self, loc):
    try:
        elements = self.driver.find_elements(*loc)
        if len(elements):
            return elements
    except:
        print u"%s 页面中未能找到 %s 元素" % (self, loc)

# 判断元素是否存在
def isElementExsit(self, loc):
    try:
        WebDriverWait(self.driver, 15).until(
            lambda driver: True if driver.find_element(*loc) is not None else False)
        # element = self.driver.find_element(*loc)
        # self.highlightElement(element)
        return True
    except:
        return False

# 定位一组元素中索引为第i个的元素 i从0开始
def find_elements_i(self, index, loc):
    try:
        elements = self.driver.find_elements(*loc)
        if elements[index] is not None:
            return elements[index]
    except:
        print u"%s 页面中未能找到%s的第 %s 个元素 " % (self, loc, index)


