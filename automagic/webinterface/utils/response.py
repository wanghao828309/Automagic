# -*- coding:utf-8 -*-

#                                                               公共                                                                                        #
SYSTEM_ERROR = {
    "code": "9999",
    "success": False,
    "msg": "System Error"
}
DATA_TO_LONG = {
    'code': '9001',
    'success': False,
    'msg': '数据信息过长！'
}

KEY_MISS = {
    "code": "9002",
    "success": False,
    "msg": "请求参数错误"
}


GENERAL_MESS = {
    'code': '1002',
    'success': False,
    'msg': ''
}

#                                                                debugtalk                                                                                    #
DEBUGTALK_NOT_EXISTS = {
    "code": "0002",
    "success": False,
    "msg": "miss debugtalk"
}

DEBUGTALK_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "debugtalk更新成功"
}

#                                                                API                                                                                        #
API_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': 'API添加成功'
}


API_NOT_FOUND = {
    'code': '0002',
    'success': False,
    'msg': '未查询到该API'
}

API_DEL_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': 'API删除成功'
}

API_UPDATE_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': 'API更新成功'
}

#                                                                用例                                                                                        #
CASE_NOT_FOUND = {
    'code': '0002',
    'success': False,
    'msg': '未查询到该用例'
}

CASE_DEL_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '用例删除成功'
}

CASE_UPDATE_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '用例更新成功'
}
CASE_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '用例添加成功'
}

SUITE_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': 'Suite添加成功'
}

SUITE_DEL_SUCCESS = {
    'code': '0003',
    'success': True,
    'msg': 'Suite删除成功'
}
SUITE_NOT_FOUND = {
    'code': '0002',
    'success': False,
    'msg': '未查询到该Suite'
}

#环境ENV
#
CONFIG_EXISTS = {
    "code": "0101",
    "success": False,
    "msg": "此环境已存在，请重新命名"
}

CONFIG_ADD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '环境添加成功'
}

CONFIG_NOT_EXISTS = {
    "code": "0102",
    "success": False,
    "msg": "指定的环境不存在"
}

CONFIG_UPDATE_SUCCESS = {
    "code": "0002",
    "success": True,
    "msg": "环境更新成功"
}
PAGESIZE_NOT_INTEGER = {
    "code": "0112",
    "success": False,
    "msg": "頁面大小或當前頁面不是整形"
}

#                                                                file                                                                                       #
FILE_UPLOAD_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': '文件上传成功'
}

FILE_EXISTS = {
    'code': '0002',
    'success': False,
    'msg': '文件已存在'
}

FILE_IS_NONE = {
    'code': '0002',
    'success': False,
    'msg': '上传的文件为空'
}

FILE_NOT_EXISTS = {
    'code': '0002',
    'success': False,
    'msg': '文件不存在'
}

#                                                                其他                                                                                       #
MUDULE_NOT_EXISTS = {
    "code": "0002",
    "success": False,
    "msg": "模块不存在"
}



RUN_ASYNC_SUCCESS = {
    'code': '0001',
    'success': True,
    'msg': 'runner执行中，请稍后查看报告即可,默认当前时间命名报告'
}

RUN_CASE_FAIL = {
    'code': '0002',
    'success': False,
    'msg': 'CASE运行失败'
}

RUN_CASE_NONE = {
    'code': '0002',
    'success': False,
    'msg': '请先选择中case或suite'
}


REPORT_UPLOAD_FAIL = {
    'code': '0002',
    'success': False,
    'msg': 'Html报告上传到服务器失败'
}