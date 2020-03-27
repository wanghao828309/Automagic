# -*- coding: utf-8 -*-

import time, datetime
import os, sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
import paramiko
import re
from FtpUp import myFtp


if sys.platform.startswith('win'):
    import win32com.client
    from uiautomation import *
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def check_db(process_name):
    """
    判断进程是否存在
    """
    from sqldb import Database
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    mydb = Database('192.168.11.83', 3306, 'root', 'root', 'Wang_Test')
    if len(processCodeCov) > 0:
        mydb.execNoQuery('INSERT INTO crashTable(crashId) VALUES(1); ')
    else:
        print ('%s is close' % process_name)
        mydb.execNoQuery('INSERT INTO crashTable(crashId) VALUES(0); ')

def check_exsit(process_name):
    """
    判断进程是否存在
    """
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        return True
    else:
        print ('%s is close' % process_name)
        return False

def close_process(process_name):
    """
    Close all process by process name.
    """
    if sys.platform.startswith('win'):
        res = check_exsit(process_name)
        # print res
        try:
            if res == True:
                print ('%s is open' % process_name)
                os.system('taskkill /f /im "{}"' .format(process_name))
                time.sleep(1)
        except Exception:
            print ('%s is close' % process_name)
    else:
        AppiumCMD = '''osascript<<END
            on is_running(appName)
            	tell application "System Events" to (name of processes) contains appName
            end is_running

            set safRunning to is_running("AppiumForMac")
            if not safRunning then
            	do shell script "open /Applications/AppiumForMac.app"
            	return "Not Running"
            end if'''
        # 启动前先杀掉退出失败的Wondershare Filmora Scrn进程
        try:
            # os.system("osascript -e 'tell application \"{}\" to quit'".format(process_name))
            os.system("pkill -f \"{}\"".format(process_name))
        except Exception as e:
            print e
        # 若AppiumForMac意外退出，则启动AppiumForMac
        # time.sleep(1.5)
        # os.system(AppiumCMD)
        # time.sleep(1)

class Action(object):
    keyword2action = {}

    def __init__(self):
        # option = webdriver.ChromeOptions()
        # option.add_argument('test-type')
        # self.driver = webdriver.Chrome(chrome_options=option)
        # self.driver = webdriver.PhantomJS()
        self.driver = None

    def __del__(self):
        pass
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
        # close_process("chrome.exe")

    @classmethod
    def add_action(cls, keyword):
        def deco(func):
            def _deco(*args, **kwargs):
                print args[1]
                return func(*args, **kwargs)

            cls.keyword2action[keyword] = _deco
            return _deco

        return deco

    # saveScreenshot:通过图片名称，进行截图保存
    def saveScreenshot(self, name):
        """
        快照截图
        name:图片名称
        """
        pngName = self.savePngName(name)
        if self.driver is not None:
            # 截图无法在浏览器里显示
            # image = self.driver.save_screenshot(pngName)
            from PIL import ImageGrab
            im = ImageGrab.grab()
            image = im.save(pngName)
        else:
            if sys.platform.startswith('win'):
                image = GetRootControl().CaptureToImage(pngName)

        # 拷贝文件到服务器
        try:
            ftp = myFtp('192.168.11.83')
            ftp.Login('wanghao', '123456')  # 登录，如果匿名登录则用空串代替即可
            fileList = pngName.split("/")
            # print 'fileList： /home/wanghao/report/html/image/'+fileList[-1]
            ftp.UpLoadFile(pngName, '/home/wanghao/report/html/image/' + fileList[-1])
            ftp.close()
        except Exception as err:
            print "报错截图上传到服务器失败:" + err.message

        return image

    # 生成图片的名称
    def savePngName(self, name):
        """
        name：自定义图片的名称
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fp = "keyword/result/" + day + "/image"
        tm = self.saveTime()
        file_type = ".png"
        # 判断存放截图的目录是否存在，如果存在打印并返回目录名称，如果不存在，创建该目录后，再返回目录名称
        if os.path.exists(fp):
            filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
            #在html报告中链接截图
            print filename
        else:
            os.makedirs(fp)
            filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
            # 在html报告中链接截图
            print filename
        return filename

    # 生成log
    def save_runing_log(self, text):
        """
        :param text:
        :return:
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        running_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        file_type = "running.log"
        fp = "result/" + day
        # print "当前工作路径："+os.path.abspath('.')
        if os.path.exists(fp):
            filename = str(fp) + "/" + str(file_type)
            with open(filename, "a") as f:
                f.write(running_time + "  " + text + '\n')
            # os.system("echo " + running_time + "  " + text + ">> " + filename)
        else:
            os.makedirs(fp)
            filename = str(fp) + "/" + str(file_type)
            # os.system("echo " + running_time + "  "  + text + ">> " + filename)
            with open(filename, "a") as f:
                f.write(running_time + "  " + text + '\n')

    # 生成图片的名称
    def saveVideoName(self, name):
        """
        name：自定义图片的名称
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fp = "keyword/result/" + day + "/image"
        tm = self.saveTime()
        file_type = ".ogv"
        # 判断存放截图的目录是否存在，如果存在打印并返回目录名称，如果不存在，创建该目录后，再返回目录名称
        if os.path.exists(fp):
            filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
        else:
            os.makedirs(fp)
            filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
        return filename

    # 获取系统当前时间
    def saveTime(self):
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
            self.find_element(loc).send_keys(value)
        except Exception as e:
            raise e
            return

    # 重写定义send_keys方法
    def write_keys(self, loc, value):
        try:
            self.mouClick(loc)
            time.sleep(0.5)
            # self.find_element(loc).send_keys(value)
            self.sendKeyboard(value)
        except Exception as e:
            raise e
            return

    # 重写元素定位方法
    def find_element(self, loc):
        for i in xrange(3):
            try:
                element = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc))
                # self.highlightElement(element)
                print element
                return element
            except Exception as e:
                raise e


    # 重写一组元素定位方法
    def find_elements(self, loc):
        try:
            elements = self.driver.find_elements(*loc)
            if len(elements):
                return elements
        except Exception as e:
            raise e
            # print u"%s 页面中未能找到 %s 元素" % (self, loc)

    # 判断元素是否存在
    def isElementExsit(self, loc,time=10):
        try:
            self.driver.implicitly_wait(float(time))
            WebDriverWait(self.driver, float(time)).until(
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


    def sendKeyboard(self,key):
        '''输出键盘键'''
        ActionChains(self.driver).send_keys(key).perform()
        time.sleep(0.5)

    def sendGroupKeyboard(self,key):
        '''输出键盘组合键'''

        if len(key)==2:
            ActionChains(self.driver).key_down(key[0]).send_keys(key[1]).perform()
            ActionChains(self.driver).key_up(key[0]).perform()
        else:
            ActionChains(self.driver).key_down(key[0]).key_down(key[1]).send_keys(key[2]).perform()
            ActionChains(self.driver).key_up(key[0]).key_up(key[1]).perform()
        time.sleep(0.5)

    def mouClick(self,loc,val=1):
        '''鼠标左键点击'''
        actions = ActionChains(self.driver)
        if val == 1:
            actions.click(self.find_element(loc))
        else:
            actions.double_click(self.find_element(loc))
        actions.perform()

    def mouxyClick(self,loc,x=0,y=0):
        '''鼠标左键点击'''
        actions = ActionChains(self.driver)
        if x!=0 and y!=0:
            actions.move_to_element_with_offset(self.find_element(loc),x,y)
            actions.click()
        else:
            actions.click(self.find_element(loc))
        actions.perform()

    def mouRightClick(self,loc,x=0,y=0):
        '''鼠标右键点击'''
        actions = ActionChains(self.driver)
        if x!=0 and y!=0:
            actions.move_to_element_with_offset(self.find_element(loc),x,y)
            actions.context_click()
        else:
            actions.context_click(self.find_element(loc))
        actions.perform()

if __name__ == '__main__':
    # driver = webdriver.Remote(command_executor='http://localhost:4622/wd/hub', desired_capabilities={'platform': 'Mac'})
    # driver.save_screenshot('1.png')
    from PIL import ImageGrab
    im = ImageGrab.grab()
    im.save("2.png")
