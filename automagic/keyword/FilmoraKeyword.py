# -*- coding: utf-8 -*-
"""
__author__ = 'wanghao'
2018-10-10
"""
from Base import *
import subprocess
import platform, re
from workSpace.utils import mediaInfoUtil

if sys.platform.startswith('win'):
    from workSpace.filmoraWin.page import startPage
    from workSpace.filmoraWin.page import homePage
    from workSpace.filmoraWin.page import inputWinPage
    from workSpace.filmoraWin.page import settingPage
    from workSpace.filmoraWin.page import exportPage
    from uiautomation import *
else:
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


# 判断在win还是MAC上运行
sysstr = platform.system()
# 当前工作路径
workPath = os.path.abspath(".")
# 存放资源个数
res_num = []
# 存放media的loacl
Local = []
# 存放导出资源的path
res_path = []
# 存放导出资源的time
res_time = []


################################################################################
# 关键字函数必须用Aciton.add_action(keyword)装饰起进行装饰
# 函数的形参必须为4个:action_object(Aciton对象), step_desc(步骤描述信息，可用于记录log),
#                  value(需要输入的值，多个输入值用逗号隔开), loc(元素的定位信息)
# 函数正常退出时不能有返回值（使用默认的返回值None），出错时返回字符串（记录出错信息）
################################################################################


##############################################################################################
#                                                                                             #
#                                 自定义关键字  START                                             #
#                                                                                             #
##############################################################################################
# 删除登录缓存
def del_cookie():
    if (sysstr == "Windows"):
        path = os.path.join(os.path.expanduser("~"), 'Documents\Wondershare Filmora 9')
        file = path + "\FConfig.ini"
        if os.path.exists(file):
            with open(file, 'r') as r:
                lines = r.readlines()
            with open(file, 'w') as w:
                for l in lines:
                    if 'Token' not in l:
                        w.write(l)
    else:
        file = "/Users/ws/Library/Preferences/com.wondershare.filmora.plist"
        if os.path.exists(file):
            os.system("/usr/libexec/PlistBuddy -c 'Delete :WSIDToken' " + file)


@Action.add_action('open_filmora')
@repeatTime(1)
def open_filmora(action_object, step_desc, value, loc):
    """
    打开filmora程序
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    time.sleep(1)
    if value.lower() == "n" or value.lower() == "no":
        del_cookie()
    if (sysstr == "Windows"):
        close_process("Wondershare Filmora9.exe")
        check_db("BsSndRpt64.exe")
        close_process("BsSndRpt64.exe")
        subprocess.Popen('C:\Program Files\Wondershare\Filmora9\Wondershare Filmora9.exe')
        # if not startPage.filmoraWindow.Exists(0, 0):
        #     subprocess.Popen('C:\Program Files\Wondershare\Filmora 9\Wondershare Filmora 9.exe')
        #     time.sleep(0.1)
        # else:
        #     print "filmora is open"
        time.sleep(3)
        start_Page = startPage.page()
        # if platform.release() == "7":
        #     start_Page.get_filmora9Control().Click()
        # 判断是否出现上次打开未保存，自动备份的提示窗口
        if WaitForExist(start_Page.get_backupControl(), 10):
            value = start_Page.get_backupControl().CurrentValue()
            # print value
            if "An automatic backup" in value:
                start_Page.get_backup_no_Control().Click()

    else:
        close_process("Wondershare Filmora9")
        action_object.driver = webdriver.Remote(command_executor='http://localhost:4622/wd/hub',
                                                desired_capabilities={'platform': 'Mac','mouseMoveSpeed':100})
        action_object.driver.get("Wondershare Filmora9")
        # 判断是否出现上次打开未保存，自动备份的提示窗口
        print loc
        if action_object.isElementExsit(loc):
            print u'自动保存窗口存在'
            action_object.find_element(loc).click()
        else:
            print u'自动保存窗口不存在'


@Action.add_action('clickNewProject_filmora')
@repeatTime(1)
def clickNewProject_filmora(action_object, step_desc, value, loc):
    """
    点击启动界面New Project图标
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        # start_Page.get_filmora9Control().Click()
        if WaitForExist(start_Page.filmoraWindow, 20):
            # if filmoraWindow.Exists(0, 0):
            start_Page.filmoraWindow.SetFocus()
            start_Page.get_newProjectControl().Click()
        else:
            return "filmora 没有成功打开"



@Action.add_action('clickOpenProject_filmora')
@repeatTime(1)
def clickOpenProject_filmora(action_object, step_desc, value, loc):
    """
    点击启动界面Open Project图标
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        if platform.release() == "7":
            start_Page.get_filmora9Control().Click()
        if WaitForExist(start_Page.filmoraWindow, 20):
            start_Page.filmoraWindow.SetFocus()
            start_Page.get_openProjectControl().Click()
        else:
            return "filmora 没有成功打开"


@Action.add_action('sendStartSeach_filmora')
@repeatTime(1)
def sendStartSeach_filmora(action_object, step_desc, value, loc):
    """
    在启动界面search搜索框里输入内容
    :param action_object:
    :param step_desc:
    :param value: text
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        if WaitForExist(start_Page.get_searchControl(), 20):
            start_Page.filmoraWindow.SetFocus()
            print "定位到启动界面search搜索框"
            start_Page.get_searchControl().Click()
            SendKeys(value)


@Action.add_action('clickStart_ProLibrary_filmora')
@repeatTime(1)
def clickStart_ProLibrary_filmora(action_object, step_desc, value, loc):
    """
    点击启动界面第n个project library
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        if WaitForExist(start_Page.get_proLibraryControl(int(value)), 20):
            start_Page.get_proLibraryControl(int(value)).DoubleClick()
        else:
            return "启动界面第：" + str(value) + " 个project library不存在"


@Action.add_action('clickClose_filmora')
@repeatTime(1)
def clickClose_filmora(action_object, step_desc, value, loc):
    """
    点击主界面右上角关闭【x】按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        home_Page = homePage.page()
        if WaitForExist(start_Page.filmoraWindow, 10):
            start_Page.filmoraWindow.SetFocus()
            home_Page.get_closeControl().Click()


@Action.add_action('clickMinOrMax_filmora')
@repeatTime(1)
def clickMinOrMax_filmora(action_object, step_desc, value, loc):
    """
    点击主界面右上角关闭【最小化/最大化】按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        start_Page = startPage.page()
        home_Page = homePage.page()
        if WaitForExist(start_Page.filmoraWindow, 20):
            home_Page.get_minOrMaxControl().Click()


# win窗口切换到指定目录下
def jumpHost(value):
    inputWin_Page = inputWinPage.page()
    if WaitForExist(inputWin_Page.get_hostControl(), 20):
        inputWin_Page.get_hostControl().Click(ratioX=0.9)
        if value is None or value == "":
            sourcePath = workPath + r"\keyword\workSpace\filmora_project\resource"
            SendKeys(sourcePath)
        else:
            SendKeys(value)
        Win32API.PressKey(uiautomation.Keys.VK_RETURN)


# 判断是否弹出创建代理窗口
def judge_proxy():
    home_Page = homePage.page()
    time.sleep(1)
    if WaitForExist(home_Page.get_proxyFail_text_Control(), 5):
        assert "Proxy creation failed" not in home_Page.get_proxyFail_text_Control().CurrentValue(), "导入文件创建proxy失败"


@Action.add_action('sendHost_filmora')
@repeatTime(1)
def sendHost_filmora(action_object, step_desc, value, loc):
    """
    在工程打开win端窗口输入保存工程地址，键盘敲击enter
    :param action_object:
    :param step_desc:
    :param value:url
    :param loc:
    """
    if (sysstr == "Windows"):
        jumpHost(value)


@Action.add_action('selectFilder_byName_filmora')
@repeatTime(1)
def selectFilder_byName_filmora(action_object, step_desc, value, loc):
    """
    根据name，双击所选择的资源文件
    :param action_object:
    :param step_desc:
    :param value:text
    :param loc:
    """
    if (sysstr == "Windows"):
        inputWin_Page = inputWinPage.page()
        filder = inputWin_Page.get_floderControl_by_name(value)
        if WaitForExist(filder, 10):
            filder.DoubleClick()
        else:
            return "输入文件名称为：" + str(value) + " 在当前目录不存在"
        try:
            judge_proxy()
        except AssertionError as e:
            return e


@Action.add_action('selectFilder_filmora')
@repeatTime(1)
def selectFilder_filmora(action_object, step_desc, value, loc):
    """
    选择当前目录下的资源，点击导入
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        inputWin_Page = inputWinPage.page()
        if WaitForExist(inputWin_Page.get_fileControl(value), 10):
            inputWin_Page.get_fileControl(value).Click()
        else:
            return "当前目录下不存在第:" + str(value) + " 资源文件"
        time.sleep(0.5)
        SendKey(Keys.VK_ENTER)
        time.sleep(0.5)
        MoveTo(400, 400)
        # inputWin_Page.get_openControl().Click()
        try:
            judge_proxy()
        except AssertionError as e:
            return e


@Action.add_action('selectAllFilder_filmora')
@repeatTime(1)
def selectAllFilder_filmora(action_object, step_desc, value, loc):
    """
    选择当前目录下全部资源，点击导入
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        inputWin_Page = inputWinPage.page()
        if WaitForExist(inputWin_Page.get_fileControl(1), 10):
            inputWin_Page.get_fileControl(1).Click()
        else:
            return "当前目录下为空"
        SendKeys('{ctrl}a')
        controls = inputWin_Page.get_floderControl().GetChildren()
        num = 0
        for control in controls:
            if control.ControlTypeName == "ListItemControl":
                num = num + 1
        res_num.append(num)
        print "当前导入资源的个数为： " + str(num)
        time.sleep(0.5)
        SendKey(Keys.VK_ENTER)
        time.sleep(0.5)
        MoveTo(400, 400)
        # inputWin_Page.get_openControl().Click()
        try:
            judge_proxy()
        except AssertionError as e:
            return e


@Action.add_action('clickFilder_filmora')
@repeatTime(1)
def clickFilder_filmora(action_object, step_desc, value, loc):
    """
    选择当前目录（推荐在桌面），点击确定
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        inputWin_Page = inputWinPage.page()
        if WaitForExist(inputWin_Page.get_folderComputerControl("本地磁盘 (D:)"), 10):
            inputWin_Page.get_folderComputerControl("本地磁盘 (D:)").Click(ratioX=-0.4)
            inputWin_Page.get_folderComputerControl(value).Click()
            inputWin_Page.get_folderSureControl().Click()
        else:
            return "浏览文件夹窗口:本地磁盘 (D:)未找到"


@Action.add_action('clickMediaRecord_filmora')
@repeatTime(1)
def clickMediaRecord_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Record列表按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaRecordControl(), 10):
            home_Page.get_mediaRecordControl().Click()
        else:
            return "media资源区Record列表按钮未找到"


@Action.add_action('clickMediaRecord_fromWebcam_filmora')
@repeatTime(1)
def clickMediaRecord_fromWebcam_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Record列表下Record from Webcam.. 选项,录制完成点击ok
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaRecord_fromWebcamControl(), 10):
            home_Page.get_mediaRecord_fromWebcamControl().Click()
            home_Page.get_RecordFromWebcam_start_Control().Click()
            time.sleep(int(value) + 3)
            home_Page.get_RecordFromWebcam_OK_Control().Click()
        else:
            return "Record列表下Record from Webcam.. 选项未找到"


@Action.add_action('clickMediaRecord_PCScreen_filmora')
@repeatTime(1)
def clickMediaRecord_PCScreen_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Record列表下Record PC Screen...选项,录制完成点击ok
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaRecord_PCScreenControl(), 10):
            home_Page.get_mediaRecord_PCScreenControl().Click()
            home_Page.get_PCScreenControl_start_Control().Click()
            time.sleep(int(value) + 3)
            Win32API.SendKey(Keys.VK_F9)
        else:
            return "Record列表下Record PC Screen... 选项未找到"
        if WaitForExist(home_Page.get_PCScreenControl_cloes_Control(), 10):
            home_Page.get_PCScreenControl_cloes_Control().Click()
        else:
            return "Record列表下Record PC Screen...选项，窗口下右上角【x】按钮未找到"


@Action.add_action('clickMediaRecord_voiceover_filmora')
@repeatTime(1)
def clickMediaRecord_voiceover_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Record列表下Record Voiceover选项,录制完成点击ok
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaRecord_voiceoverControl(), 10):
            home_Page.get_mediaRecord_voiceoverControl().Click()
        else:
            return "Record列表下Record Voiceover选项未找到"
        if WaitForExist(home_Page.get_RecordVoiceover_start_Control(), 10):
            home_Page.get_RecordVoiceover_start_Control().Click()
            time.sleep(int(value) + 3)
            home_Page.get_RecordVoiceover_start_Control().Click()
            home_Page.get_RecordVoiceover_OK_Control().Click()
        else:
            return "Record列表下Record Voiceover选项，窗口start图标未找到"


@Action.add_action('clickImportMedia_filmora')
@repeatTime(1)
def clickImportMedia_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import Media Files Here图标
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_importMediaControl(), 10):
            home_Page.get_importMediaControl().DoubleClick()
        else:
            return "资源区Import Media Files Here不存在"


@Action.add_action('clickMediaImport_filmora')
@repeatTime(1)
def clickMediaImport_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImportControl(), 10):
            home_Page.get_mediaImportControl().Click()
        else:
            return "media资源区Import列表按钮未找到"


@Action.add_action('clickMediaImport_files_filmora')
@repeatTime(1)
def clickMediaImport_files_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表下Import Media Files... Ctrl+I选项
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImport_filesControl(), 10):
            home_Page.get_mediaImport_filesControl().Click()
        else:
            return "media资源区Import列表下Import Media Files... Ctrl+I选项未找到"


@Action.add_action('clickMediaImport_floder_filmora')
@repeatTime(1)
def clickMediaImport_floder_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表下Import a Media Folder...选项
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImport_folderControl(), 10):
            home_Page.get_mediaImport_folderControl().Click()
        else:
            return "media资源区Import列表下Import a Media Folder...选项未找到"


def import_internet(value, sign):
    home_Page = homePage.page()
    home_Page.get_internet_signControl().Click()
    if sign.lower() == "facebook":
        facebook_window = home_Page.get_Facebook_titleControl()
        if WaitForExist(facebook_window, 10):
            print facebook_window.Name
            username = value.split(":")[0]
            passwd = value.split(":")[1]
            time.sleep(3)
            SendKey(Keys.VK_TAB)
            SendKey(Keys.VK_TAB)
            SendKey(Keys.VK_TAB)
            SendKeys(username)
            SendKey(Keys.VK_TAB)
            SendKeys(passwd)
            SendKey(Keys.VK_ENTER)
            time.sleep(2)
            SendKey(Keys.VK_ENTER)
            if WaitForExist(facebook_window, 3):
                SendKey(Keys.VK_TAB)
                SendKey(Keys.VK_TAB)
                SendKey(Keys.VK_TAB)
                SendKey(Keys.VK_ENTER)
        else:
            return "【sign in】到Facebook窗口未成功"
        i = 1
        while i <= 10:
            i += 1
            if WaitForExist(facebook_window, 10):
                SendKey(Keys.VK_ENTER)
                time.sleep(2)
            else:
                break
    elif sign.lower() == "instagram":
        instagram_window = home_Page.get_Instagram_textControl()
        if WaitForExist(instagram_window, 30):
            print instagram_window.Name
            username = value.split(":")[0]
            passwd = value.split(":")[1]
            time.sleep(2)
            home_Page.get_Instagram_phone_editControl().Click()
            # SendKey(Keys.VK_TAB)
            SendKeys(username)
            SendKey(Keys.VK_TAB)
            SendKeys(passwd)
            SendKey(Keys.VK_ENTER)
            time.sleep(2)
            SendKey(Keys.VK_ENTER)
        else:
            return "【sign in】到instagram窗口未成功"
        i = 1
        while i <= 10:
            i += 1
            if WaitForExist(instagram_window, 10):
                SendKey(Keys.VK_ENTER)
                time.sleep(2)
            else:
                break
    elif sign.lower() == "flickr":
        flickr_window = home_Page.get_Flickr_textControl()
        if WaitForExist(flickr_window, 20):
            print flickr_window.Name
            username = value.split(":")[0]
            passwd = value.split(":")[1]
            time.sleep(5)
            SendKeys(username)
            SendKey(Keys.VK_ENTER)
            time.sleep(2)
            SendKeys(passwd)
            SendKey(Keys.VK_ENTER)
            if WaitForExist(home_Page.get_acceptBtnControl(), 20):
                home_Page.get_acceptBtnControl().Click()
            else:
                return "Download Photos from Flickr....窗口下的【好的，我授權】按钮未找到"
        else:
            return "【sign in】到Flick窗口未成功"
    elif sign.lower() == "youtube":
        export_Page = exportPage.page()
        youtube_window = export_Page.get_YouTube_textControl()
        if WaitForExist(youtube_window, 20):
            username = value.split(":")[0]
            passwd = value.split(":")[1]
            time.sleep(5)
            SendKeys(username)
            SendKey(Keys.VK_ENTER)
            time.sleep(2)
            SendKeys(passwd)
            SendKey(Keys.VK_ENTER)
        else:
            return "【sign in】到youtube窗口未成功"
        i = 1
        while i <= 10:
            i += 1
            if WaitForExist(youtube_window, 10):
                SendKey(Keys.VK_ENTER)
                time.sleep(2)
            else:
                break
        # if WaitForExist(export_Page.get_YouTube_allowControl(), 10):
        #     SendKey(Keys.VK_TAB)
        #     SendKey(Keys.VK_TAB)
        #     SendKey(Keys.VK_TAB)
        #     SendKey(Keys.VK_TAB)
        #     SendKey(Keys.VK_TAB)
        #     SendKey(Keys.VK_ENTER)


@Action.add_action('clickMediaImport_Facebook_filmora')
@repeatTime(1)
def clickMediaImport_Facebook_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表下Download Media from Facebook...选项，并且导入资源，点击import
    :param action_object:
    :param step_desc:
    :param value:list
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImport_FacebookControl(), 10):
            home_Page.get_mediaImport_FacebookControl().Click()
        else:
            return "media资源区Import列表下Download Media from Facebook...选项未找到"
        if WaitForExist(home_Page.get_internet_signControl(), 10):
            time.sleep(2)
            name = home_Page.get_internet_signControl().Name
        else:
            return "Download Media from Facebook...界面下【sign in/sign out】按钮未找到"
        print("界面下【sign in/sign out】按钮的值为:" + name)
        if "SIGN IN" in name:
            import_internet(value, "facebook")
        res_list = home_Page.get_internet_ListControl()
        if WaitForExist(res_list, 20):
            i = 1
            while i <= 10:
                i += 1
                text = home_Page.get_internet_fileTextControl().Name
                if "0" not in text:
                    print "Download Media from Facebook...界面下【Files Selected】内容为：" + str(text)
                    home_Page.get_internet_importControl().Click()
                    break
                elif i <= 10:
                    # print i
                    time.sleep(2)
                else:
                    return "Download Media from Facebook...界面下【Files Selected】内容为：" + str(text)
        else:
            return "Download Media from Facebook...界面下,未成功导入资源"


@Action.add_action('clickMediaImport_Instagram_filmora')
@repeatTime(1)
def clickMediaImport_Instagram_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表下Download Media from Instagram...选项，并且导入资源，点击import
    :param action_object:
    :param step_desc:
    :param value:list
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImport_InstagramControl(), 10):
            home_Page.get_mediaImport_InstagramControl().Click()
        else:
            return "media资源区Import列表下Download Media from Instagram...选项未找到"
        if WaitForExist(home_Page.get_internet_signControl(), 10):
            time.sleep(2)
            name = home_Page.get_internet_signControl().Name
        else:
            return "Download Media from Instagram...界面下【sign in/sign out】按钮未找到"
        print("界面下【sign in/sign out】按钮的值为:" + name)
        if "SIGN IN" in name:
            import_internet(value, "instagram")
        res_list = home_Page.get_internet_ListControl()
        if WaitForExist(res_list, 20):
            i = 1
            while i <= 10:
                i += 1
                text = home_Page.get_internet_fileTextControl().Name
                if "0" not in text:
                    print "Download Media from Instagram...界面下【Files Selected】内容为：" + str(text)
                    num = re.findall(r"\d+\.?\d*", text)[0]
                    res_num.append(num)
                    home_Page.get_internet_importControl().Click()
                    break
                elif i <= 10:
                    # print i
                    time.sleep(2)
                else:
                    return "Download Media from Instagram...界面下【Files Selected】内容为：" + str(text)
        else:
            return "Download Media from Instagram...界面下,未成功导入资源"


@Action.add_action('clickMediaImport_Flickr_filmora')
@repeatTime(1)
def clickMediaImport_Flickr_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区Import列表下Download Media from Flickr...选项，并且导入资源，点击import
    :param action_object:
    :param step_desc:
    :param value:list
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaImport_FlickrControl(), 10):
            home_Page.get_mediaImport_FlickrControl().Click()
        else:
            return "media资源区Import列表下Download Media from Flickr...选项未找到"
        if WaitForExist(home_Page.get_internet_signControl(), 10):
            time.sleep(2)
            name = home_Page.get_internet_signControl().Name
        else:
            return "Download Media from Flickr...界面下【sign in/sign out】按钮未找到"
        print("界面下【sign in/sign out】按钮的值为:" + name)
        if "SIGN IN" in name:
            import_internet(value, "flickr")
        res_list = home_Page.get_internet_ListControl()
        if WaitForExist(res_list, 20):
            i = 1
            while i <= 10:
                i += 1
                text = home_Page.get_internet_fileTextControl().Name
                if "0" not in text:
                    print "Download Media from Flickr...界面下【Files Selected】内容为：" + str(text)
                    num = re.findall(r"\d+\.?\d*", text)[0]
                    res_num.append(num)
                    home_Page.get_internet_importControl().Click()
                    break
                elif i <= 10:
                    # print i
                    time.sleep(2)
                else:
                    return "Download Media from Flickr...界面下【Files Selected】内容为：" + str(text)
        else:
            return "Download Media from Flickr...界面下,未成功导入资源"


@Action.add_action('clickRightImport_filmora')
@repeatTime(1)
def clickRightImport_filmora(action_object, step_desc, value, loc):
    """
    点击home界面media资源区右键【import】选项
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        home_Page.get_mediaListControl().RightClick()
        if WaitForExist(home_Page.get_menuItemControl('Import'), 10):
            home_Page.get_menuItemControl('Import').Click()
        else:
            return "home界面media资源区右键【import】选项未找到"


@Action.add_action('clickProjectModify_filmora')
@repeatTime(1)
def clickProjectModify_filmora(action_object, step_desc, value, loc):
    """
    点击修改保存工程窗口（project is modify, do you want to save project?）的yes或者no按钮
    :param action_object:
    :param step_desc:
    :param value:yes or no
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if str(value).lower() in ["yes", "y"]:
            home_Page.get_proModifyYesControl().Click()
        elif str(value).lower() in ["no", "n"]:
            home_Page.get_proModifyNoControl().Click()
        else:
            home_Page.get_proModifyCancelControl().Click()


@Action.add_action('clickFile_filmora')
@repeatTime(1)
def clickFile_filmora(action_object, step_desc, value, loc):
    """
    点击home界面【file】选项
    :param action_object:
    :param step_desc:
    :param value:text
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_fileControl(), 10):
            home_Page.get_fileControl().Click()
        else:
            return "home界面菜单【file】未找到"



@Action.add_action('clickEXPORT_filmora')
@repeatTime(1)
def clickEXPORT_filmora(action_object, step_desc, value, loc):
    """
    点击home界面【EXPORT】选项
    :param action_object:
    :param step_desc:
    :param value:text
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_EXPORTControl(), 10):
            home_Page.get_EXPORTControl().Click()
        else:
            return "home界面菜单【EXPORT】未找到"


@Action.add_action('click_exportClose_filmora')
@repeatTime(1)
def click_exportClose_filmora(action_object, step_desc, value, loc):
    """
    点击export界面获取右上角【x】按钮
    :param action_object:
    :param step_desc:
    :param value:text
    :param loc:
    """
    if (sysstr == "Windows"):
        export_Page = exportPage.page()
        if WaitForExist(export_Page.get_closeControl(), 10):
            export_Page.get_closeControl().Click()
        else:
            return " 点击export界面获取右上角【x】按钮未找到"


@Action.add_action('clickProSetting_filmora')
@repeatTime(1)
def clickProSetting_filmora(action_object, step_desc, value, loc):
    """
    点击home界面【file】下【Project Settings】选项
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_proSetControl(), 10):
            home_Page.get_proSetControl().Click()
        else:
            return "home界面【file】下【Project Settings】未找到"



@Action.add_action('selectProSetting_filmora')
@repeatTime(1)
def selectProSetting_filmora(action_object, step_desc, value, loc):
    """
    在【Project Settings】界面，设置Resolution与Frame Rate
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        setting_Page = settingPage.page()
        setting_Page.get_resolutionControl().Select("3840 x 2160 (4k UHD)")
        setting_Page.get_frameRateControl().Select("23.97 fps")
        setting_Page.get_OKControl().Click()


@Action.add_action('clickFile_importFile_filmora')
@repeatTime(1)
def clickFile_importFile_filmora(action_object, step_desc, value, loc):
    """
    点击home界面【file】下【Import Media】的【Import Media Files... Ctrl+I】
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_fileImport_Control(), 20):
            home_Page.get_file_importFile_Control().Click()
        else:
            return "home界面【file】下【Import Media】的【Import Media Files... Ctrl+I】未找到"


@Action.add_action('clickError_close_filmora')
@repeatTime(1)
def clickError_close_filmora(action_object, step_desc, value, loc):
    """
    点击home界面导入格式不支持的文件时是否弹窗（Errors Information）-->【CLOSE】按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_errorCloseControl(), 10):
            home_Page.get_errorCloseControl().Click()
        else:
            return "home界面导入格式不支持的文件时是否弹窗（Errors Information）-->【CLOSE】按钮未找到"


def get_local(data):
    x = (int(data[0]) + int(data[2])) / 2
    y = (int(data[1]) + int(data[3])) / 2
    return (x, y)


# 获取importMedia区的local
def getImportMedia_local():
    home_Page = homePage.page()
    if WaitForExist(home_Page.get_importMediaControl(), 10):
        local = get_local(home_Page.get_importMediaControl().BoundingRectangle)
        Local.append(local)
    else:
        raise Exception, "资源区Import Media Files Here不存在"


# 通过win+r快捷键打开运行窗口导入文件
def get_file(value, x, y):
    SendKeys('{Win}r')
    while not isinstance(GetFocusedControl(), EditControl):
        time.sleep(1)
    # sourcePath = workPath + r"\workSpace\filmora_project\resource"
    sourcePath = workPath + r"\keyword\workSpace\filmora_project\resource"
    SendKeys(sourcePath + '{Enter}')
    inputWin_Page = inputWinPage.page()
    minOrMaxControl = inputWin_Page.get_minOrMaxControl()
    print minOrMaxControl.Name
    if minOrMaxControl.Name == "最大化":
        inputWin_Page.get_maxControl().Click()
    time.sleep(1)
    DragDrop(800, 10, 1000, 650)
    if WaitForExist(inputWin_Page.get_floderControl_by_name(value), 10):
        ListItem = inputWin_Page.get_floderControl_by_name(value)
        ListItem.Click()
        local = get_local(ListItem.BoundingRectangle)
        # print local
    else:
        raise Exception, "名称为：" + value + " 的文件，在当前目录不存在"
    DragDrop(local[0], local[1], x, y)
    inputWin_Page.get_minControl().Click()


@Action.add_action('importFile_filmora')
@repeatTime(1)
def importFile_filmora(action_object, step_desc, value, loc):
    """
    通过win+r快捷键打开运行窗口，在打开目录下导入文件media区
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    getImportMedia_local()
    if (sysstr == "Windows"):
        get_file(value, Local[0][0], Local.pop(0)[1])


def getTimeLine_local():
    home_Page = homePage.page()
    if WaitForExist(home_Page.get_timelineControl(), 10):
        local = get_local(home_Page.get_timelineControl().BoundingRectangle)
        Local.append(local)
    else:
        raise Exception, "未正确定位到时间线"


@Action.add_action('importFile_timeline_filmora')
@repeatTime(1)
def importFile_timeline_filmora(action_object, step_desc, value, loc):
    """
    通过win+r快捷键打开运行窗口，在打开目录下导入文件到时间线
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        getTimeLine_local()
        get_file(value, Local[0][0], Local.pop(0)[1])
        time.sleep(1)


@Action.add_action('dragRes_timeline_filmora')
@repeatTime(1)
def dragRes_timeline_filmora(action_object, step_desc, value, loc):
    """
    通过拖拽资源区资源到时间线
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        getTimeLine_local()
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideo_firstControl(), 10):
            firstRes = home_Page.get_simpleVideo_firstControl()
            firstRes.DoubleClick()
            res_loacl = get_local(firstRes.BoundingRectangle)
            DragDrop(res_loacl[0], res_loacl[1], Local[0][0] + 200, Local.pop(0)[1])
            SendKey(Keys.VK_ENTER)
            time.sleep(1)
        else:
            return "home界面media资源区没有资源"


@Action.add_action('rightClick_timeline_filmora')
@repeatTime(1)
def rightClick_timeline_filmora(action_object, step_desc, value, loc):
    """
    通过右键---->insert资源区资源到时间线
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideo_firstControl(), 10):
            firstRes = home_Page.get_simpleVideo_firstControl()
            firstRes.DoubleClick()
            time.sleep(0.5)
            firstRes.RightClick()
            home_Page.get_menuItemControl("Insert").Click()
            SendKey(Keys.VK_ENTER)
            # timeline.MoveCursor(t_loacl[0]+200,t_loacl[1])
            time.sleep(1)
        else:
            return "home界面media资源区没有资源"


@Action.add_action('middleClick_timeline_filmora')
@repeatTime(1)
def middleClick_timeline_filmora(action_object, step_desc, value, loc):
    """
    点击资源区资源中间【+】按钮添加到时间线
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideo_firstControl(), 10):
            firstRes = home_Page.get_simpleVideo_firstControl()
            firstRes.DoubleClick()
            firstRes.Click(ratioY=0.4)
            SendKey(Keys.VK_ENTER)
            time.sleep(1)
        else:
            return "home界面media资源区没有资源"


@Action.add_action('import_simpleVideo_filmora')
@repeatTime(1)
def import_simpleVideo_filmora(action_object, step_desc, value, loc):
    """
    选中home界面【simple video】列表选项-->first video，右键insert到时间线
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideoControl(), 10):
            home_Page.get_simpleVideoControl().Click()
            home_Page.get_simpleVideo_firstControl().Click()
            SendKeys("{shift}i")
            # SendKey(Keys.VK_ENTER)
        else:
            return "home界面【simple video】列表选项未找到"
        if WaitForExist(home_Page.get_proSetting_notControl(), 10):
            home_Page.get_proSetting_notControl().Click()
        else:
            return "home界面 工程帧率自动匹配窗口 【DON'T CHANGE】按钮未找到"


@Action.add_action('delete_file_filmora')
@repeatTime(1)
def delete_file_filmora(action_object, step_desc, value, loc):
    """
    选中media资源区资源，添加到时间线，快捷键删除
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideo_firstControl(), 10):
            home_Page.get_simpleVideo_firstControl().Click()
            SendKeys("{shift}i")
            SendKey(Keys.VK_ENTER)
            time.sleep(1)
            home_Page.get_simpleVideo_firstControl().Click()
            SendKey(Keys.VK_DELETE)
            SendKey(Keys.VK_ENTER)
        else:
            return "home界面media资源区没有资源"


@Action.add_action('rightDelete_file_filmora')
@repeatTime(1)
def rightDelete_file_filmora(action_object, step_desc, value, loc):
    """
    选中media资源区资源，右键-->delete删除
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_simpleVideo_firstControl(), 10):
            home_Page.get_simpleVideo_firstControl().RightClick()
            home_Page.get_menuItemControl('Delete').Click()
            SendKey(Keys.VK_ENTER)
        else:
            return "home界面media资源区没有资源"


@Action.add_action('search_file_filmora')
@repeatTime(1)
def search_file_filmora(action_object, step_desc, value, loc):
    """
    选中media资源区search搜索框，输入内容搜索
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_searchControl(), 10):
            home_Page.get_searchControl().DoubleClick()
            time.sleep(0.5)
            SendKeys(value)
        else:
            return "media资源区search搜索框未找到"


@Action.add_action('typeSelect_filmora')
@repeatTime(1)
def typeSelect_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区右上角资源类别选项，分别选择video，image，audio
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_typeSelectControl(), 10):
            home_Page.get_typeSelectControl().DoubleClick()
            if value.lower() == "video":
                home_Page.get_typeSelect_VideoControl().Click()
                print "选择video"
            elif value.lower() == "image":
                home_Page.get_typeSelect_ImageControl().Click()
                print "选择image"
            else:
                home_Page.get_typeSelect_AudioControl().Click()
                print "选择audio"
        else:
            return "media资源区右上角资源类别选项图标未找到"


@Action.add_action('viewSelect_groupbyType_filmora')
@repeatTime(1)
def viewSelect_groupbyType_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区右上角view切换选项--->Group by--->type
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_viewSelectControl(), 10):
            home_Page.get_viewSelectControl().DoubleClick()
            home_Page.get_viewSelectControl().MoveCursor(ratioY=80)
            # home_Page.get_menuItemControl("Group by").Click()
            time.sleep(0.5)
            home_Page.get_viewSelectControl().MoveCursor(ratioY=80, ratioX=150)
            if value.lower() == "type":
                print "type"
                home_Page.get_menuItemControl("Type").Click()
            else:
                home_Page.get_menuItemControl("None").Click()
        else:
            return "media资源区右上角view切换选项图标未找到"


@Action.add_action('media_addFloder_filmora')
@repeatTime(1)
def media_addFloder_filmora(action_object, step_desc, value, loc):
    """
    点击media资源区左下角添加文件夹图标，重命名新增的文件夹
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_media_addFloder_Control(), 10):
            home_Page.get_media_addFloder_Control().Click()
            SendKeys(value)
            time.sleep(0.5)
            SendKey(Keys.VK_ENTER)


@Action.add_action('save_project_filmora')
@repeatTime(1)
def save_project_filmora(action_object, step_desc, value, loc):
    """
    保存工程文件到指定的地址
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        SendKeys("{ctrl}s")
        print "value" + value
        if value != "":
            inputWin_Page = inputWinPage.page()
            if WaitForExist(inputWin_Page.get_hostControl(), 20):
                inputWin_Page.get_hostControl().Click(ratioX=0.9)
                SendKeys(value)
                time.sleep(0.5)
                SendKey(Keys.VK_ENTER)
            else:
                return "win端打开文件夹窗口地址栏输入框未找到"
        SendKey(Keys.VK_ENTER)
        time.sleep(0.5)
        MoveTo(400, 400)
        time.sleep(0.5)


@Action.add_action('select_exportHost_filmora')
@repeatTime(1)
def select_exportHost_filmora(action_object, step_desc, value, loc):
    """
    在export窗口，选择导出资源文件的路径
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        export_Page = exportPage.page()
        inputWin_Page = inputWinPage.page()
        if WaitForExist(export_Page.get_saveToControl(), 10):
            export_Page.get_saveToControl().Click()
        else:
            return "export窗口未找到【save to】图标按钮"
        if WaitForExist(inputWin_Page.get_export_hostControl(), 10):
            # inputWin_Page.get_export_hostControl().Click()
            sourcePath = workPath + r"\keyword\workSpace\filmora_project\export"
            if not os.path.exists(sourcePath):
                os.mkdir(sourcePath)
            res_path.append(sourcePath)
            SendKeys(sourcePath)
            res = res_path[0] + "\My Video.wmv"
            for root, dirs, files in os.walk(sourcePath, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            Win32API.PressKey(uiautomation.Keys.VK_RETURN)
            time.sleep(0.5)
            inputWin_Page.get_export_selectFloderControl().Click()
            # time.sleep(0.5)
            # Win32API.PressKey(uiautomation.Keys.VK_RETURN)
        else:
            return "export窗口，点击【save to】图标按钮，弹出win窗口地址输入框未找到"


@Action.add_action('export_resource_filmora')
@repeatTime(1)
def export_resource_filmora(action_object, step_desc, value, loc):
    """
    在export窗口，点击export，导出资源文件
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        export_Page = exportPage.page()
        if WaitForExist(export_Page.get_exportControl(), 10):
            export_Page.get_exportControl().Click()
        else:
            return "export窗口，点击【export】图标未找到"


@Action.add_action('export_inputName_filmora')
@repeatTime(1)
def export_inputName_filmora(action_object, step_desc, value, loc):
    """
    在export窗口，name输入框，输入内容
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    export_Page = exportPage.page()
    if WaitForExist(export_Page.get_NameEditControl(), 10):
        export_Page.get_NameEditControl().Click()
        SendKeys('{ctrl}a')
        Win32API.PressKey(uiautomation.Keys.VK_BACK)
        export_Page.get_NameEditControl().SendKeys(value)
    else:
        return "export窗口，点击【export】图标未找到"


@Action.add_action('uesrlogin_filmora')
@repeatTime(1)
def uesrlogin_filmora(action_object, step_desc, value, loc):
    """
    home界面，点击用户登录图标，输入用户名，密码，登录
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """

    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_loginIcon_Control(), 10):
            home_Page.get_loginIcon_Control().Click()
        else:
            return "home界面菜单栏登录图标未找到"

        if WaitForExist(home_Page.get_loginTitle_Control(), 20):
            # time.sleep(1)
            SendKey(Keys.VK_TAB)
            # home_Page.get_emailInput_Control().Click()
            SendKeys("wanghao@wondershare.cn")
            SendKey(Keys.VK_TAB)
            SendKeys("123456")
            time.sleep(0.5)
            SendKey(Keys.VK_RETURN)
            # home_Page.get_loginButton_Control().Click()
        else:
            return "home界面登录窗口未找到"



@Action.add_action('clickFile_Preference_filmora')
@repeatTime(1)
def clickFile_Preference_filmora(action_object, step_desc, value, loc):
    """
    点击home界面【file】下【Preference】
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_menuItemControl("Preference"), 20):
            home_Page.get_menuItemControl("Preference").Click()
        else:
            return "点击home界面【file】下【Preference】未找到"



@Action.add_action('select_ProGpuProxy_filmora')
@repeatTime(1)
def select_PreGpuProxy_filmora(action_object, step_desc, value, loc):
    """
    在【Preference】窗口，切换到Performance界面，选中GPU与Proxy
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_checkBoxControl("Performance"), 20):
            home_Page.get_checkBoxControl("Performance").Click()
        else:
            return "home界面【file】下【Preference】未找到"

        cpu = home_Page.get_checkBoxControl("Enable GPU Acceleration")
        print "VALUE:" + value
        if value != "":
            cpu_v = value.split(",")[0]
            porxy_v = value.split(",")[1]
        else:
            cpu_v, porxy_v = "", ""
        if WaitForExist(cpu, 20):
            if cpu_v.lower() in ["n", "no"]:
                if cpu.CurrentToggleState():
                    cpu.Click()
                    print "GPU关闭"
            else:
                if not cpu.CurrentToggleState():
                    cpu.Click()
                    print "GPU打开"
        else:
            return "home界面【file】下【Preference】下的GPU复选框未找到"
        proxy = home_Page.get_checkBoxControl("Automatically create proxies")
        if WaitForExist(proxy, 20):
            if porxy_v.lower() in ["n", "no"]:
                if proxy.CurrentToggleState():
                    proxy.Click()
                    print "proxy关闭"
            else:
                if not proxy.CurrentToggleState():
                    proxy.Click()
                    print "proxy打开"
        else:
            return "home界面【file】下【Preference】下的proxy复选框未找到"
        home_Page.get_ok_Control().Click()




@Action.add_action('select_check_filmora')
@repeatTime(1)
def select_check_filmora(action_object, step_desc, value, loc):
    """
    检查复选框是否选中
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        cpu = home_Page.get_checkBoxControl("Enable GPU Acceleration")
        print "VALUE:" + value
        if value != "":
            cpu_v = value.split(",")[0]
            porxy_v = value.split(",")[1]
        else:
            cpu_v, porxy_v = "", ""
        if WaitForExist(cpu, 20):
            if cpu_v.lower() in ["n", "no"]:
                if cpu.CurrentToggleState():
                    cpu.Click()
                    print "GPU关闭"
            else:
                if not cpu.CurrentToggleState():
                    cpu.Click()
                    print "GPU打开"
        else:
            return "home界面【file】下【Preference】下的GPU复选框未找到"
        proxy = home_Page.get_checkBoxControl("Automatically create proxies")
        if WaitForExist(proxy, 20):
            if porxy_v.lower() in ["n", "no"]:
                if proxy.CurrentToggleState():
                    proxy.Click()
                    print "proxy关闭"
            else:
                if not proxy.CurrentToggleState():
                    proxy.Click()
                    print "proxy打开"
        else:
            return "home界面【file】下【Preference】下的proxy复选框未找到"
    else:
        print loc
        ele = action_object.find_element(loc)
        if value not in ["n", "no"]:
            # print ele.get_attribute("AXValue"),ele.get_attribute("AXType"),ele.get_attribute("AXDescription")
            if ele.get_attribute("AXValue") == "0":
                print "元素处于未选中状态"
                ele.click()
            else:
                print "元素处于选中状态"
        else:
            if ele.get_attribute("AXValue") == "0":
                print "元素处于未选中状态"
            else:
                print "元素处于选中状态"
                ele.click()

@Action.add_action('click_PreferenceClose_filmora')
@repeatTime(1)
def click_PreferenceClose_filmora(action_object, step_desc, value, loc):
    """
    点击【Preference】窗口【X】按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        home_Page.get_ok_Control().Click()



@Action.add_action('export_YouTube_filmora')
@repeatTime(1)
def export_YouTube_filmora(action_object, step_desc, value, loc):
    """
    导出资源到YouTube，输入账户，密码，登录YouTube，点击export
    :param action_object:
    :param step_desc:
    :param value:list
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_checkBoxControl("YouTube"), 10):
            home_Page.get_checkBoxControl("YouTube").Click()
        else:
            return "export窗口【YouTube】选项未找到"
        if WaitForExist(home_Page.get_internet_signControl(), 10):
            time.sleep(2)
            name = home_Page.get_internet_signControl().Name
        else:
            return "export窗口【YouTube】界面下【sign in/sign out】按钮未找到"
        print("界面下【sign in/sign out】按钮的值为:" + name)
        if "SIGN IN" in name:
            import_internet(value, "YouTube")


@Action.add_action('click_loginclose_btn')
def click_loginclose_btn(action_object, step_desc, value, loc):
    """
    点击登录窗口关闭按钮
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    :return:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        home_Page.get_loginClose_Control().Click()



# ————————————————————————————————
# v开头的为assert方法
# ————————————————————————————————
@Action.add_action('v_mediaResNum_filmora')
@repeatTime(1)
def v_mediaResNum_filmora(action_object, step_desc, value, loc):
    """
    【验证】media资源区，资源个数
    :param action_object:
    :param step_desc:
    :param value:int
    :param loc:
    """
    if (sysstr == "Windows"):
        if value == "" or value is None:
            value = res_num.pop(0)
        home_Page = homePage.page()
        time.sleep(1)
        if WaitForExist(home_Page.get_mediaListControl(), 10):
            num = len(home_Page.get_mediaListControl().GetChildren())
            # print value
            if num == int(value):
                print "【验证】通过，media资源区资源个数正确：" + str(num)
            else:
                return "【验证】失败，media资源区资源个数不正确：" + str(num)
        else:
            return "未找到资源区资源"


@Action.add_action('v_importFile_disapear_filmora')
@repeatTime(1)
def v_importFile_disapear_filmora(action_object, step_desc, value, loc):
    """
    【验证】导入资源时弹出的import files窗口
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        if value == "" or value is None:
            time = 10
        else:
            time = int(value)
        home_Page = homePage.page()
        if WaitForDisappear(home_Page.get_importFilesControl(), time):
            print "【验证】通过 importFiles窗口在：" + str(time) + " 秒内消失"

        else:
            return "【验证】失败 importFiles窗口在：" + str(time) + " 秒内未消失"


@Action.add_action('v_importFromInstagram_disapear_filmora')
@repeatTime(1)
def v_importFromInstagram_disapear_filmora(action_object, step_desc, value, loc):
    """
    【验证】在Download Media from Instagram，导入资源时弹出的Download Media from Instagram....窗口
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        if value == "" or value is None:
            times = 10
        else:
            times = int(value)
        home_Page = homePage.page()
        if WaitForDisappear(home_Page.get_importFromInstagramControl(), times):
            print "【验证】通过 Download Media from Instagram....窗口在：" + str(times) + " 秒内消失"
        else:
            return "【验证】失败 Download Media from Instagram....窗口在：" + str(times) + " 秒内未消失"


@Action.add_action('v_importFromFlickr_disapear_filmora')
@repeatTime(1)
def v_importFromFlickr_disapear_filmora(action_object, step_desc, value, loc):
    """
    【验证】在Download Media from Flickr，导入资源时弹出的Download Media from Flickr....窗口
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        if value == "" or value is None:
            time = 10
        else:
            time = int(value)
        home_Page = homePage.page()
        if WaitForDisappear(home_Page.get_importFromFlickrControl(), time):
            print "【验证】通过 Download Media from Flickr....窗口在：" + str(time) + " 秒内消失"

        else:
            return "【验证】失败 Download Media from Flickr....窗口在：" + str(time) + " 秒内未消失"


@Action.add_action('v_projectModify_filmora')
@repeatTime(1)
def v_projectModify_filmora(action_object, step_desc, value, loc):
    """
    【验证】关闭工程时是否弹出保存工程窗口（project is modify, do you want to save project?）
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if value.lower() == "n":
            try:

                text = home_Page.get_proModifyTextControl().CurrentValue()
                if "The project has been modified" in text:
                    return "【验证】失败 出现project is modify, do you want to save project窗口"
                else:
                    print "【验证】通过 未出现project is modify, do you want to save project窗口"
            except:
                print "【验证】通过 未出现project is modify, do you want to save project窗口"
        else:
            try:
                text = home_Page.get_proModifyTextControl().CurrentValue()
                if "The project has been modified" in text:
                    print "【验证】通过 出现project is modify, do you want to save project窗口"
                else:
                    return "【验证】失败 未出现project is modify, do you want to save project窗口"
            except:
                return "【验证】失败 未出现project is modify, do you want to save project窗口"


@Action.add_action('v_errorInformation_filmora')
@repeatTime(1)
def v_errorInformation_filmora(action_object, step_desc, value, loc):
    """
    【验证】导入格式不支持的文件时是否弹窗（Errors Information）窗口
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_errorControl(), 10):
            print "【验证】通过 已经弹出（Errors Information）窗口"

        else:
            return "【验证】失败 未出现（Errors Information）窗口"


@Action.add_action('v_projectSetting_filmora')
@repeatTime(1)
def v_projectSetting_filmora(action_object, step_desc, value, loc):
    """
    【验证】新建工程默认project setting里的值
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        setting_Page = settingPage.page()
        if WaitForExist(setting_Page.get_resolutionControl(), 10):
            print "预期结果：1920 x 1080"
            print "实际结果：" + setting_Page.get_resolutionControl().CurrentValue()
            assert "1920 x 1080" in setting_Page.get_resolutionControl().CurrentValue(), "【验证】失败 【Resolution】不为：1920 x 1080"
            print "预期结果：25 fps"
            print "实际结果：" + setting_Page.get_frameRateControl().CurrentValue()
            assert "25 fps" in setting_Page.get_frameRateControl().CurrentValue(), "【验证】失败 【Frame Rate】不为：25 fps"
            print "预期结果：16:9"
            print "实际结果：" + setting_Page.get_aspectRadioControl().Name
            assert "16:9" in setting_Page.get_aspectRadioControl().Name, "【验证】失败 【Aspect Radio】不为：16:9"
        else:
            return "【验证】失败 未出现project setting窗口"



@Action.add_action('v_export_Framerate_filmora')
@repeatTime(1)
def v_export_Framerate_filmora(action_object, step_desc, value, loc):
    """
    【验证】export窗口的Resolution与Frame Rate的值
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        export_Page = exportPage.page()

        if WaitForExist(export_Page.get_textControl("Export to file and save on com"), 10):
            resolution = export_Page.get_resolution_textControl().Name
            frameRate = export_Page.get_frameRate_textControl().Name
            if "3840x2160" in resolution and "23.97" in frameRate:
                print "【验证】通过 export窗口Resolution的值为：{}，Frame Rate的值为：{}".format(resolution, frameRate)
            else:
                return "【验证】失败 export窗口Resolution的值为：{}，Frame Rate的值为：{}".format(resolution, frameRate)

        else:
            return "【验证】失败 export窗口打开失败"


@Action.add_action('v_groupView_filmora')
@repeatTime(1)
def v_groupView_filmora(action_object, step_desc, value, loc):
    """
    【验证】切换到分组视图是否成功
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_mediaListControl(2), 10):
            print "【验证】通过 切换到分组视图成功"

        else:
            return "【验证】失败 未成功切换到分组视图"


@Action.add_action('v_timeline_clips_filmora')
@repeatTime(1)
def v_timeline_clips_filmora(action_object, step_desc, value, loc):
    """
    【验证】时间线上是否存在clips
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        getTimeLine_local()
        RightClick(Local[0][0] + 200, Local.pop(0)[1])
        if WaitForExist(home_Page.get_menuItemControl("Show Properties"), 10):
            print "【验证】通过 时间线上存在clips"
        elif home_Page.get_menuItemControl("Cut").IsEnabled:
            return "【验证】失败 时间线上存在多个clips"
        else:
            return "【验证】失败 时间线上不存在clips"


@Action.add_action('v_exportNoRes_filmora')
@repeatTime(1)
def v_exportNoRes_filmora(action_object, step_desc, value, loc):
    """
    【验证】时间线为空，点击export，是否正确弹出提示框
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        home_Page = homePage.page()
        if WaitForExist(home_Page.get_exportNoRes_text_Control(), 10):
            text = home_Page.get_exportNoRes_text_Control().CurrentValue()
            if "You have no resource" in text:
                print "【验证】通过 时间线为空，点击export，弹出提示框正确：\n" + text
                home_Page.get_ok_Control().Click()
            else:
                return "【验证】失败 时间线为空，点击export，弹出提示框内容错误: \n" + text

        else:
            return "【验证】失败 时间线为空，点击export，未弹出提示框"


@Action.add_action('v_completedExport_filmora')
@repeatTime(1)
def v_completedExport_filmora(action_object, step_desc, value, loc):
    """
    【验证】export的资源是否完成
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    export_Page = exportPage.page()
    if WaitForExist(export_Page.get_completedControl(), int(value)):
        print("【验证】通过 Export:Completed")
        export_Page.get_exportCloseControl().Click()
    else:
        return "【验证】失败 Export:NO Completed"


@Action.add_action('v_completedExport_YouTobe_filmora')
@repeatTime(1)
def v_completedExport_YouTobe_filmora(action_object, step_desc, value, loc):
    """
    【验证】export的资源导出到YouTobe是否完成
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    export_Page = exportPage.page()
    url = export_Page.get_export_byName_TextControl("https://www.youtube.com")
    if WaitForExist(url, int(value)):
        print ("【验证】通过 导出完成，youtube的url正确出现:" + url.Name)
        export_Page.get_exportYoutobe_okControl().Click()
    else:
        return "【验证】失败 youtube的url没有出现"


@Action.add_action('v_comparedExport_time_filmora')
@repeatTime(1)
def v_comparedExport_time_filmora(action_object, step_desc, value, loc):
    """
    【验证】打开/关闭GPU，export的资源时间对比
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    export_Page = exportPage.page()
    if WaitForExist(export_Page.get_completedControl(), int(value)):
        print("【验证】 Export:Completed")
        res_time.append(export_Page.get_exportElapsedTimeControl().Name[-2:])
        print res_time
        if len(res_time) > 1:
            if int(res_time[1]) > int(res_time[0]):
                print "验证通过 GPU导出比CPU快,分别为{} ,{}".format(res_time.pop(0), res_time.pop(0))
            else:
                return "验证失败 GPU导出比CPU慢,分别为{} ,{}".format(res_time.pop(0), res_time.pop(0))
        export_Page.get_exportCloseControl().Click()
    else:
        return "【验证】失败 Export:NO Completed"


@Action.add_action('v_mediaInfo_resource')
@repeatTime(1)
def v_mediaInfo_resource(action_object, step_desc, value, loc):
    """
    【验证】利用mediaInfo验证导出资源的参数
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    path = res_path.pop(0) + "\My Video.mp4"
    print "文件路径是："+path
    mediaInfo = mediaInfoUtil.video_analysis(path)
    resoAc = str(mediaInfo["res_width"]) + "*" + str(mediaInfo["res_height"])
    if resoAc == "1280*720":
        print "【验证】通过 导出资源的分辨率正确：" + resoAc
    else:
        return "【验证】失败 导出资源的分辨率不一致：" + resoAc
    if '29.97' in mediaInfo["v_framerate"]:
        print "【验证】通过 导出资源的帧率正确：" + mediaInfo["v_framerate"]
    else:
        return "【验证】失败 导出资源的帧率不一致：" + mediaInfo["v_framerate"]

@Action.add_action('v_Suc_disapper')
@repeatTime(1)
def v_Suc_disapper(action_object, step_desc, value, loc):
    """
    【验证】用户登录成功窗口是否消失
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    if (sysstr == "Windows"):
        pass
    else:
        print loc
        i=1
        while(i<10):
            if not action_object.isElementExsit(loc):
                break
            else:
                time.sleep(0.5)
                i=i+1

@Action.add_action('v_loginSuc_filmora')
@repeatTime(1)
def v_loginSuc_filmora(action_object, step_desc, value, loc):
    """
    【验证】用户Lifetime登录是否成功
    :param action_object:
    :param step_desc:
    :param value:
    :param loc:
    """
    home_Page = homePage.page()
    if WaitForDisappear(home_Page.get_loginTitle_Control(), 10):
        print "用户登录窗口成功消失"
    else:
        return "用户登录窗口未消失"
    time.sleep(1)
    home_Page.get_loginIcon_Control().Click()
    try:
        if WaitForExist(home_Page.get_loginSuc_textControl(), 10):
            print("【验证】通过 Lifetime用户成功登录")
            home_Page.get_loginClose_Control().Click()
    except:
        return "【验证】失败 Lifetime用户未成功登录"



#                                                                                             #
#                                 自定义关键字  END                                             #
##############################################################################################

if __name__ == '__main__':
    # startPage.page().get_filmora9Control().Click()
    # time.sleep(1)
    # open_filmora("", "", "n", "")
    # clickNewProject_filmora("", "", "", "")
    # clickMediaImport_filmora("", "", 1, "")
    # judge_proxy()
    print open_filmora("", "", "", "")
    # v_mediaResNum_filmora("", "", "", "")
    # v_loginSuc_filmora("", "", "", "")
    # v_completedExport_filmora("", "", "30", "")
    # print v_mediaInfo_resource("", "", "", "")
    pass
