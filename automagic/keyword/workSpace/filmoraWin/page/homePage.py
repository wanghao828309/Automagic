#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

if sys.platform.startswith('win'):
    from uiautomation import *


class page:
    def __init__(self):
        self.paneControl = PaneControl(searchDepth=2, ClassName='Qt5QWindowIcon')

    # home界面【file】选项
    def get_fileControl(self):
        return MenuItemControl(searchFromControl=self.paneControl, searchDepth=4, Name='File')

    # home界面【file】下【Project Settings】
    def get_proSetControl(self):
        return MenuItemControl(Name='Project Settings')

    # home界面【file】下【Import Media】
    def get_fileImport_Control(self):
        return MenuItemControl(Name='Import Media')

    # home界面【file】下【Import Media】的【Import Media Files... Ctrl+I】
    def get_file_importFile_Control(self):
        MenuItemControl(Name='Import Media').MoveCursor()
        # time.sleep(0.5)
        menuControl = MenuControl(ClassName="Qt5QWindowPopupSaveBits")
        return MenuItemControl(searchFromControl=menuControl, foundIndex=1)
        # return MenuItemControl(SubName="Import Media Files")

    # home界面右上角【x】按钮
    def get_closeControl(self):
        return ButtonControl(searchFromControl=self.paneControl, searchDepth=4, foundIndex=4)

    # home界面右上角【最小化/最大化】按钮
    def get_minOrMaxControl(self):
        return ButtonControl(searchFromControl=self.paneControl, searchDepth=4, foundIndex=2)

    # home界面media资源区资源列表
    def get_mediaListControl(self, index=1):
        return ListControl(searchFromControl=self.paneControl, foundIndex=index)

    # home界面media资源区search搜索框
    def get_searchControl(self):
        return EditControl(searchFromControl=self.paneControl)

    # home界面media资源区Import Media Files Here图标
    def get_importMediaControl(self):
        return TextControl(searchFromControl=self.paneControl, Name="Import Media Files Here")

    # home界面media资源区Import列表按钮
    def get_mediaImportControl(self):
        return CustomControl(searchFromControl=self.paneControl, foundIndex=13)

    # home界面media资源区Import列表下Import Media Files... Ctrl+I选项
    def get_mediaImport_filesControl(self):
        return MenuItemControl(SubName="Import Media Files")

    # home界面media资源区Import列表下Import a Media Folder...选项
    def get_mediaImport_folderControl(self):
        return MenuItemControl(SubName="Import a Media Folder")

    # home界面media资源区Import列表下Import with Instant Cutter Tool…选项
    # def get_mediaImport_cutterControl(self):
    #     return MenuItemControl(SubName="Import with Instant Cutter Tool")

    # home界面media资源区Import列表下Download Media from Facebook...选项
    def get_mediaImport_FacebookControl(self):
        return MenuItemControl(SubName="Download Media from Facebook")

    # home界面media资源区Import列表下Download Photos from Instagram...选项
    def get_mediaImport_InstagramControl(self):
        return MenuItemControl(SubName="Download Photos from Instagram")

    # home界面media资源区Import列表下Download Photos from Flickr...选项
    def get_mediaImport_FlickrControl(self):
        return MenuItemControl(SubName="Download Photos from Flickr")

    # home界面media资源区Import列表下Download Media from Facebook/Instagram...，打开界面下【sign in/sign out】按钮
    def get_internet_signControl(self):
        return ButtonControl(searchFromControl=self.paneControl, foundIndex=2)

    # home界面media资源区Import列表下Download Media from Facebook/Instagram...，打开界面下【Files Selected】内容
    def get_internet_fileTextControl(self):
        return TextControl(searchFromControl=self.paneControl, SubName="Files Selected")

    # home界面media资源区Import列表下Download Media from Facebook/Instagram....，打开界面下video的个数
    def get_internet_ListControl(self):
        return ListItemControl(searchFromControl=self.paneControl)

    # home界面media资源区Import列表下Download Media from Facebook/Instagram....，打开界面下【import】按钮
    def get_internet_importControl(self):
        return ButtonControl(searchFromControl=self.paneControl, Name="Import")

    # home界面media资源区Import列表下Download Media from Facebook...，打开界面下【sign in】窗口下的Facebook Authorization的title
    def get_Facebook_titleControl(self):
        return TextControl(Name="Facebook Authorization")

    # home界面media资源区Import列表下Download Media from Instagram..，打开界面下【sign in】窗口下的"Login • Instagram的窗口
    def get_Instagram_textControl(self):
        return TextControl(Name="Instagram Authorization")

    # Instagram的窗口的Phone number, username, or ema... 输入框
    def get_Instagram_phone_editControl(self):
        return EditControl(SubName="Phone number")

    # home界面在Download Media from Instagram，导入资源时弹出的Download Media from Instagram....窗口
    def get_importFromInstagramControl(self):
        return PaneControl(SubName="Download Photos from Instagram", searchDepth=1)

    # home界面在Download Media from Flickr，打开界面下【sign in】窗口下的的Download Photos from Flickr....窗口
    def get_Flickr_textControl(self):
        return TextControl(Name="Flickr Authorization")

    # home界面在Download Media from Flickr，打开界面下【sign in】窗口下的的Download Photos from Flickr....【好的，我授權】按钮
    def get_acceptBtnControl(self):
        return ButtonControl(SubName="好的，我授權")

    # home界面在Download Media from Flickr，导入资源时弹出的Download Media from Flickr....窗口
    def get_importFromFlickrControl(self):
        return PaneControl(SubName="Download Photos from Flickr", searchDepth=1)

    # home界面media资源区Import列表下Import with Instant Cutter Tool…，打开界面下【open file】图标
    def get_Cutter_openControl(self):
        return WindowControl(Name="Filmora Instant Cutter")

    # home界面media资源区Record列表按钮
    def get_mediaRecordControl(self):
        return CustomControl(searchFromControl=self.paneControl, foundIndex=14)

    # home界面media资源区Record列表下Record from Webcam.. 选项
    def get_mediaRecord_fromWebcamControl(self):
        return MenuItemControl(SubName="Record from Webcam")

    # home界面media资源区Record列表下Record PC Screen...选项
    def get_mediaRecord_PCScreenControl(self):
        return MenuItemControl(SubName="Record PC Screen")

    # home界面media资源区Record列表下Record Voiceover选项
    def get_mediaRecord_voiceoverControl(self):
        return MenuItemControl(SubName="Record Voiceover")

    # home界面media资源区Record列表下Record from Webcam.. 选项，窗口下start图标
    def get_RecordFromWebcam_start_Control(self):
        return CheckBoxControl(ClassName="Qt5QWindowIcon")

    # home界面media资源区Record列表下Record from Webcam.. 选项，窗口下OK按钮
    def get_RecordFromWebcam_OK_Control(self):
        return ButtonControl(ClassName="Qt5QWindowIcon", Name="OK")

    # home界面media资源区Record列表下Record PC Screen...选项，窗口下start图标
    def get_PCScreenControl_start_Control(self):
        PaneControl(Name="Wondershare Filmora Scrn").SetFocus()
        return CheckBoxControl(searchFromControl=PaneControl(Name="Wondershare Filmora Scrn"), foundIndex=4)

    # home界面media资源区Record列表下Record PC Screen...选项，窗口下右上角【x】按钮
    def get_PCScreenControl_cloes_Control(self):
        return ButtonControl(searchFromControl=PaneControl(Name="Wondershare Filmora Scrn"), searchDepth=2,
                             foundIndex=2)

    # home界面media资源区Record列表下Record Voiceover选项，窗口下start图标
    def get_RecordVoiceover_start_Control(self):
        return CheckBoxControl(searchFromControl=self.paneControl)

    # home界面media资源区Record列表下Record Voiceover选项，窗口下OK按钮
    def get_RecordVoiceover_OK_Control(self):
        return ButtonControl(searchFromControl=self.paneControl, Name="OK")

    # home界面导入资源时弹出的import file窗口
    def get_importFilesControl(self):
        return PaneControl(Name="Importing files", searchDepth=1)

    # home界面关闭工程时弹出的project is modify, do you want to save project?窗口的text内容
    def get_proModifyTextControl(self):
        return EditControl(searchFromControl=self.paneControl, searchDepth=5)

    # home界面关闭工程时弹出的project is modify, do you want to save project?窗口的yes按钮
    def get_proModifyYesControl(self):
        return ButtonControl(searchFromControl=self.paneControl, Name="YES Enter", searchDepth=4)

    # home界面关闭工程时弹出的project is modify, do you want to save project?窗口的no按钮
    def get_proModifyNoControl(self):
        return ButtonControl(searchFromControl=self.paneControl, Name="NO", searchDepth=4)

    # home界面关闭工程时弹出的project is modify, do you want to save project?窗口的cancel按钮
    def get_proModifyCancelControl(self):
        return ButtonControl(searchFromControl=self.paneControl, Name="CANCEL", searchDepth=4)

    # home界面导入格式不支持的文件时是否弹窗（Errors Information）窗口
    def get_errorControl(self):
        return PaneControl(Name="Errors Information", searchDepth=1)

    # home界面导入格式不支持的文件时是否弹窗（Errors Information）-->【CLOSE】按钮
    def get_errorCloseControl(self):
        return ButtonControl(Name="CLOSE Enter", searchDepth=2)

    # home界面【EXPORT】按钮
    def get_EXPORTControl(self):
        return ButtonControl(Name="EXPORT")

    # home界面【simple video】列表选项
    def get_simpleVideoControl(self):
        return TreeItemControl(searchFromControl=self.paneControl, foundIndex=4)

    # home界面【simple video】列表选项-->first video
    def get_simpleVideo_firstControl(self):
        return ListItemControl(searchFromControl=self.paneControl, foundIndex=1)

    # home界面工程帧率自动匹配窗口【DON'T CHANGE】按钮
    def get_proSetting_notControl(self):
        return ButtonControl(searchFromControl=PaneControl(Name="Project Setting"), Name="DON'T CHANGE")

    # home界面media资源区右上角资源类别选项
    def get_typeSelectControl(self):
        return CustomControl(searchFromControl=self.paneControl, foundIndex=5)

    # home界面media资源区右上角资源类别选项--->video
    def get_typeSelect_VideoControl(self):
        return MenuItemControl(Name="Video")

    # home界面media资源区右上角资源类别选项--->Audio
    def get_typeSelect_AudioControl(self):
        return MenuItemControl(Name="Audio")

    # home界面media资源区右上角资源类别选项--->Image
    def get_typeSelect_ImageControl(self):
        return MenuItemControl(Name="Image")

    # home界面media资源区右上角view切换选项
    def get_viewSelectControl(self):
        return ButtonControl(searchFromControl=self.paneControl, foundIndex=5)

    # 通过name匹配MenuItemControl
    def get_menuItemControl(self, name):
        return MenuItemControl(SubName=name)

    # 通过name匹配CheckBoxControl
    def get_checkBoxControl(self, name):
        return CheckBoxControl(searchFromControl=self.paneControl, SubName=name)

    # home界面video时间线
    def get_timelineControl(self):
        return TextControl(Name='1')

    # home界面media添加文件夹图标
    def get_media_addFloder_Control(self):
        return ButtonControl(searchFromControl=self.paneControl, foundIndex=1)

    # home界面菜单栏登录图标
    def get_loginIcon_Control(self):
        return ButtonControl(searchFromControl=self.paneControl, foundIndex=5, searchDepth=4)

    # home界面登录窗口标题
    def get_loginTitle_Control(self):
        return PaneControl(ClassName='Chrome_WidgetWin_0')

    # # home界面登录窗口用户名输入框
    # def get_emailInput_Control(self):
    #     docControl = DocumentControl(Name=u'登陆注册')
    #     return EditControl(searchFromControl=docControl, foundIndex=1)
    #
    # # home界面登录窗口密码输入框
    # def get_paswordInput_Control(self):
    #     return EditControl(Name="Password")
    #
    # # home界面登录窗口login按钮
    # def get_loginButton_Control(self):
    #     return ButtonControl(Name="Login")

    # home界面登录成功窗口状态显示text
    def get_loginSuc_textControl(self):
        return TextControl(Name="Lifetime Plan")

    # home界面登录窗口右上角【x】按钮
    def get_loginClose_Control(self):
        return ButtonControl(searchFromControl=self.paneControl)

    # home界面，弹窗提示框窗口【OK】按钮
    def get_ok_Control(self):
        return ButtonControl(searchFromControl=self.paneControl, SubName="OK")

    # home界面时间线为空，点击export，弹出提示框窗口文本内容
    def get_exportNoRes_text_Control(self):
        return EditControl(searchFromControl=self.paneControl)

    # home界面导入资源，创建proxy失败时弹窗的内容
    def get_proxyFail_text_Control(self):
        return EditControl(searchFromControl=self.paneControl)


if __name__ == '__main__':
    time.sleep(2)
    print re.findall(r"\d+\.?\d*", "Files Selected: 8 file(s)")[0]
    # page().get_resSelect_VideoControl().Click()
