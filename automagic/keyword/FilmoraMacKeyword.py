# -*- coding: utf-8 -*-
"""
__author__ = 'wanghao'
2018-10-10
"""
from Base import *
import subprocess
import platform, re
from workSpace.utils import mediaInfoUtil
from workSpace.filmoraMac.page import mhomePage
from workSpace.filmoraMac.page import mstartPage
from workSpace.filmoraMac.page import mpreferencesPage


def repeatTime(arg):
    """
    装饰器：用于对方法的装饰，包括（1.捕获方法的异常输出的html报告 2.控制方法出错重复执行）
    :param arg: int（出错重复执行的次数）
    :return:
    """

    def decorator(func):
        def wrapper(*args, **kw):
            for i in range(int(arg)):
                try:
                    if i > 0:
                        print ("第 " + str(i) + " 次重试")
                    r = func(*args, **kw)
                    return r
                except Exception as err:
                    time.sleep(3)
                    print('【Exception】 The one case fail by :%s' % err.message)
            raise Exception

        return wrapper

    return decorator


################################################################################
# 关键字函数必须用Aciton.add_action(keyword)装饰起进行装饰
# 函数的形参必须为4个:action_object(Aciton对象), step_desc(步骤描述信息，可用于记录log),
#                  value(需要输入的值，多个输入值用逗号隔开), loc(元素的定位信息)
# 函数正常退出时不能有返回值（使用默认的返回值None），出错时返回字符串（记录出错信息）
################################################################################


##############################################################################################
#                                                                                             #
#                                 自定义关键字  START                                           #
#                                                                                             #
##############################################################################################

# ————————————————————————————————
# 通用方法
# ————————————————————————————————



@Action.add_action('sleep')
def action_sleep(action_object, step_desc, value, loc):
    """
    强制脚本等待关键字
    :param action_object:
    :param step_desc:
    :param value: 等待时间单位是秒（s），float型
    :param loc:
    :return:
    """
    time.sleep(float(value))


@Action.add_action('click_btn')
@repeatTime(1)
def click_btn(action_object, step_desc, value, loc):
    """
    点击一个元素
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    try:
        if value=="1":
            action_object.mouClick(loc)
        elif value=="2":
            action_object.mouClick(loc,2)
        else:
            action_object.find_element(loc).click()
        # print action_object.find_element(loc)
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e

@Action.add_action('Click_xy_btn')
@repeatTime(1)
def Click_xy_btn(action_object, step_desc, value, loc):
    """
    点击一个元素,指定偏移
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    if len(value)>0:
        v = value.split(",")
        action_object.mouxyClick(loc,v[0],v[1])
    else:
        action_object.mouxyClick(loc)

@Action.add_action('click_assertValue_btn')
@repeatTime(1)
def click_assertValue_btn(action_object, step_desc, value, loc):
    """
    点击一个元素,当其Value不为1时
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    try:
        ele = action_object.find_element(loc)
        print "值为："+ele.get_attribute("AXValue")
        if ele.get_attribute("AXValue")=="0":
            ele.click()
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e

@Action.add_action('click_assertTitle_btn')
@repeatTime(1)
def click_assertTitle_btn(action_object, step_desc, value, loc):
    """
    点击一个元素,当其Value不为1时
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    try:
        ele = action_object.find_element(loc)
        print "AXTitle值为："+ele.get_attribute("AXTitle")
        if ele.get_attribute("AXTitle")==value:
            ele.click()
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e


@Action.add_action('rightClick_btn')
@repeatTime(1)
def rightClick_btn(action_object, step_desc, value, loc):
    """
    右键点击一个元素
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    # print "长度为：{}".format(len(value))
    if len(value)>0:
        v = value.split(",")
        action_object.mouRightClick(loc,v[0],v[1])
    else:
        action_object.mouRightClick(loc)



@Action.add_action('send_text')
def action_InputText(action_object, step_desc, value, loc):
    """
    文本框输入内容
    :param action_object:
    :param step_desc:
    :param value: text
    :param loc:
    :return:
    """
    print loc, value
    action_object.write_keys(loc, value)
    time.sleep(0.5)
    # action_object .sendKeyboard(Keys.ENTER)




@Action.add_action('select_Option')
@repeatTime(1)
def select_Option(action_object,step_desc,value,loc):
    """
    在select选项下，选取相应的value选项
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """


    val = value.split(",")
    optionxpath = loc[1]+"[@AXTitle='"+val[0]+"']"
    loc2 = (loc[0],optionxpath)
    print loc2, val
    try:
        if len(val)>1 and val[1]=='1':
            print 1
            action_object.mouClick(loc2)
        elif len(val)>1 and val[1]=='2':
            print 2
            action_object.mouClick(loc2,2)
        else:
            action_object.find_element(loc2).click()
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e


@Action.add_action('selectTitle_DoubleClick')
@repeatTime(1)
def selectTitle_DoubleClick(action_object,step_desc,value,loc):
    """
    选取相应的value选项,双击选中
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    # print loc
    optionxpath = loc[1]+"[@AXTitle='"+value+"']"
    loc2 = (loc[0],optionxpath)
    print loc2, value
    try:
        action_object.mouClick(loc2,2)
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e



@Action.add_action('keyboard_input')
def keyboard_input(action_object, step_desc, value, loc):
    """
    键盘输入
    :param action_object:
    :param step_desc:
    :param value: text
    :param loc:
    :return:
    """
    val = value.split(",")
    val_new = []
    print val
    for v in val:
        if v.lower() =="enter":
            v = Keys.ENTER
        elif v.lower() =="command":
            v = Keys.COMMAND
        elif v.lower() =="shift":
            v = Keys.LEFT_SHIFT
        elif v.lower() =="tab":
            v = Keys.TAB
        elif v.lower() =="del":
            v = Keys.DELETE
        elif v.lower() =="space":
            v = Keys.SPACE
        else:
            v = v
        val_new.append(v)
    print val_new
    if len(val)>1:
        action_object.sendGroupKeyboard(val_new)
    else:
        action_object.sendKeyboard(val_new[0])


@Action.add_action('sign_in')
def sign_in(action_object, step_desc, value, loc):
    """
    登录
    :param action_object:
    :param step_desc:
    :param value: text
    :param loc:
    :return:
    """
    print loc, value
    try:
        ele = action_object.find_element(loc)
        print "AXTitle值为："+ele.get_attribute("AXTitle")
        if ele.get_attribute("AXTitle")==value:
            ele.click()
            loc2 = (u'xpath', u"/AXApplication[@AXTitle='Wondershare Filmora 9']/AXWindow/AXSheet/AXGroup/AXGroup/AXScrollArea/AXWebArea/AXGroup[@AXSubrole='AXLandmarkMain']/AXGroup/AXStaticText[@AXValue='\u767b\u5f55 Facebook']")
            if action_object.isElementExsit(loc2):
                print u'实际结果：元素存在'
                action_object.sendKeyboard("13575906896")
                action_object.sendKeyboard(Keys.TAB)
                action_object.sendKeyboard("wanghao82830943")
                action_object.sendKeyboard(Keys.ENTER)
                time.sleep(3)
                action_object.sendKeyboard(Keys.ENTER)
                time.sleep(2)
            else:
                print "帐号已经成功登录"
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e



@Action.add_action('system_command')
def system_command(action_object, step_desc, value, loc):
    """
    调用mac的shell命令
    :param action_object:
    :param step_desc:
    :param value:参数
    :param loc:
    :return:
    """
    existPath = value.replace("\\","").strip()
    print existPath
    if os.path.exists(existPath):
        print '文件存在'
        try:
            os.system('rm ' + str(value))
        except Exception, e:
            print e
    else:
        print "文件不存在"

@Action.add_action('uesrlogin_continue_filmora')
def uesrlogin_continue_filmora(action_object, step_desc, value, loc):
    """
    mac系统额外的登录继续窗口，点击【login】，输入用户名，密码，登录
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    # print loc
    # action_object.find_element(loc).click()
    time.sleep(0.5)
    action_object.sendKeyboard(Keys.TAB)
    action_object.sendKeyboard("wanghao@wondershare.cn")
    #兼容中文输入法
    # action_object.sendKeyboard(Keys.ENTER)
    action_object.sendKeyboard(Keys.TAB)
    action_object.sendKeyboard("123456")
    action_object.sendKeyboard(Keys.ENTER)

#-----------------------------------------------------------------


@Action.add_action('v_mac_disapper')
def v_mac_disapper(action_object, step_desc, value, loc):
    """
    【验证】窗口是否消失
    :param action_object:
    :param step_desc:
    :param value: text
    :param loc:
    :return:
    """
    print loc
    i = 0
    while (i < int(value)):
        if not action_object.isElementExsit(loc):
            print "窗口成功消失"
            break
        else:
            time.sleep(0.5)
            i = i + 1
    if i>int(value):
        return "窗口仍未消失"



@Action.add_action('assertValue')
def action_assertValue(action_object, step_desc, value, loc):
    """
    断言value是否正确
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    try:
        expected = action_object.find_element(loc).get_attribute("AXValue")
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e
    print u'预期结果：' + value
    print u'实际结果：' + expected
    if value not in expected:
        return u'实际结果和预期结果不同！'


@Action.add_action('assertEnable')
def action_assertEnable(action_object, step_desc, value, loc):
    """
    断言元素是否可用
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print loc, value
    try:
        expected = action_object.find_element(loc).get_attribute("AXEnabled")
    except Exception as e:
        print "页面中未能找到 %s 元素" % (loc)
        raise e
    print u'预期结果：' + value
    print u'实际结果：' + expected
    if value != str(expected):
        return u'实际结果和预期结果不同！'


@Action.add_action('assertExist')
def action_assertExist(action_object, step_desc, value, loc):
    """
    断言界面元素是存在的
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    print u'预期结果：元素存在'
    if len(value)==0:
        t=10
    else:
        t=value
    print loc,t
    if action_object.isElementExsit(loc,t):
        print u'实际结果：元素存在'
    else:
        return u'实际结果：元素不存在'



@Action.add_action('v_mediaInfo_macResource')
def v_mediaInfo_resource(action_object, step_desc, value, loc):
    """
    【验证】利用mediaInfo验证导出资源的参数
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    existPath = value.replace("\\","").strip()
    print existPath
    mediaInfo = mediaInfoUtil.video_analysis(existPath)
    resoAc = str(mediaInfo["res_width"]) + "*" + str(mediaInfo["res_height"])
    if resoAc == "1920*1080":
        print "【验证】通过 导出资源的分辨率正确：" + resoAc
    else:
        return "【验证】失败 导出资源的分辨率不一致：" + resoAc
    if '60' in mediaInfo["v_framerate"]:
        print "【验证】通过 导出资源的帧率正确：" + mediaInfo["v_framerate"]
    else:
        return "【验证】失败 导出资源的帧率不一致：" + mediaInfo["v_framerate"]


#                                                                                             #
#                                 自定义关键字  END                                             #
##############################################################################################

if __name__ == '__main__':
    # print os.path.exists("/Users/ws/Movies/Wondershare\ Filmora\ 9/Project/Untitled.wfp")
    val = "/Users/ws/Movies/Wondershare\ Filmora\ 9/Output/My\ Video.mov"
    # system_command("","",val,"")
    # print os.path.exists(val.replace("\\",""))
    v_mediaInfo_resource("","",val.replace("\\",""),"")
    pass
