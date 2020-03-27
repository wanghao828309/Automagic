#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
if sys.platform.startswith('win'):
    from uiautomation import *

class page:
    def __init__(self):
        self.paneControl = PaneControl(searchDepth=2, ClassName='Qt5QWindowIcon')

    # home界面【file】下【Project Settings】的【Resolution】
    def get_resolutionControl(self):
        return ComboBoxControl(searchFromControl=self.paneControl, Name=' Down', foundIndex=2)


    # home界面【file】下【Project Settings】的【Frame Rate】
    def get_frameRateControl(self):
        return ComboBoxControl(searchFromControl=self.paneControl, Name=' Down', foundIndex=3)


    # home界面【file】下【Project Settings】的【Aspect Radio】
    def get_aspectRadioControl(self):
        return ListItemControl(searchFromControl=self.paneControl, Name='16:9 (Widescreen)', foundIndex=1)

    # home界面【file】下【Project Settings】的【OK】按钮
    def get_OKControl(self):
        return ButtonControl(searchFromControl=self.paneControl, Name='OK Enter')

# def get_local(data):
#     x = (int(data[0]) + int(data[2])) / 2
#     y = (int(data[1]) + int(data[3])) / 2
#     return (x, y)
#
#
# def selectEncoder(encoder):
#     encoderComboBox = ComboBoxControl(searchDepth=3, foundIndex=1)
#     encoderComboBox.Select(encoder)
#
# def selectResolution(resolution):
#     resolutionComboBox = ComboBoxControl(searchDepth=3, foundIndex=2)
#     resolutionComboBox.Select(resolution)
#
# def selectFrameRate(frameRate):
#     frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=3)
#     frameRateComboBox.Select(frameRate)
#
# def selectFrameRate2(frameRate):
#     frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=3)
#     frameRateComboBox.Click()
#     # print frameRateComboBox.BoundingRectangle
#     ListItem = ListItemControl(searchFromControl=frameRateComboBox, foundIndex=2)
#     # print ListItem.BoundingRectangle
#     local = get_local(ListItem.BoundingRectangle)
#     MoveTo(local[0],local[1])
#     time.sleep(0.2)
#     WheelDown(2)
#     time.sleep(0.2)
#     ListItemControl(searchFromControl=frameRateComboBox, Name=frameRate).Click()
#
# def selectVideoBitrate(videoBitrate):
#     videoBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=4)
#     bool = videoBitrateComboBox.Select(videoBitrate)
#     # print(bool)
#
# def selectVideoBitrate2(videoBitrate):
#     videoBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=4)
#     videoBitrateComboBox.Click()
#     ListItem = ListItemControl(searchFromControl=videoBitrateComboBox, foundIndex=2)
#     local = get_local(ListItem.BoundingRectangle)
#     MoveTo(local[0],local[1])
#     time.sleep(0.2)
#     WheelDown(2)
#     time.sleep(0.2)
#     ListItemControl(searchFromControl=videoBitrateComboBox, Name=videoBitrate).Click()
#
# def selectAudioEncoder(audioEncoder):
#     encoderComboBox = ComboBoxControl(searchDepth=3, foundIndex=5)
#     encoderComboBox.Select(audioEncoder)
#
# def selectChannel(channel):
#     resolutionComboBox = ComboBoxControl(searchDepth=3, foundIndex=6)
#     resolutionComboBox.Select(channel)
#
# def selectSampleRate(sampleRate):
#     frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=7)
#     frameRateComboBox.Select(sampleRate)
#
# def selectAudioBitrate(audioBitrate):
#     videoBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=8)
#     videoBitrateComboBox.Select(audioBitrate)
#
# def clickDefault():
#     defaultControl = ButtonControl(searchDepth=2, Name='DEFAULT Enter')
#     defaultControl.Click()
#     time.sleep(0.5)
#
# def clickOk():
#     okControl = ButtonControl(searchDepth=2, Name='Ok'.upper())
#     okControl.Click()
#
# def getPathValue():
#     pathControl = EditControl(searchDepth=7, foundIndex=2)
#     return pathControl.CurrentValue()
#
# def getFrameRateNum():
#     ComboBoxControl(searchDepth=3, foundIndex=3).Click()
#     return len(ListControl(searchDepth=4, foundIndex=3).GetChildren())
#
# def getBitRateNum():
#     ComboBoxControl(searchDepth=3, foundIndex=4).Click()
#     return len(ListControl(searchDepth=4, foundIndex=4).GetChildren())

