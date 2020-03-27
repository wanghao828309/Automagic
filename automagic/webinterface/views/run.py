# -*- coding:utf-8 -*-
import os, sys, time
import functools, logging
from threading import Thread
from rest_framework.decorators import api_view
from rest_framework.response import Response
from httprunner import HttpRunner
from webinterface.utils import common, runner, response, ftpUp, dbUtil
import shutil

"""运行方式
"""
logger = logging.getLogger('webinterface.views')


def back_async(func):
    """异步执行装饰器
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


def ftp_file(path, fileName):
    """
    FTP上传文件
    :param path:
    :param fileName:
    :return:
    """
    ftp = ftpUp.myFtp('192.168.11.83')
    ftp.Login('wanghao', '123456')  # 登录，如果匿名登录则用空串代替即可
    # print filename
    if sys.platform.startswith('win'):
        fileList = path.split("\\")
    else:
        fileList = path.split("/")
    ftp.UpLoadFile(path, '/data/www/html/automagic/webinterface/' + fileList[-1])
    ftp.close()
    report_url = "http://192.168.11.83/automagic/webinterface/" + fileName + ".html"
    return report_url


def fact_iter(httpRunner, count, max, yaml_list=[]):
    """
    httpRunner执行失败重试
    :param httpRunner:
    :param yaml_list:
    """
    logger.info("------------------ 开始执行httpRunner ------------------")
    httpRunner.run(yaml_list)
    if not httpRunner.summary["success"] and count < max:
        time.sleep(1)
        logger.info("httpRunner运行失败，第 " + str(count + 1) + " 次重试")
        return fact_iter(httpRunner, count + 1, max, yaml_list)


def httpRunner_runner(user, path, api=False, yaml_list=[], name=""):
    """
    httpRunner执行器
    :param path:
    :return:
    """
    kwargs = {
        "failfast": False,
    }
    httpRunner = HttpRunner(**kwargs)
    # httpRunner.run(yaml_list)
    try:
        if api:
            httpRunner.run(path)
            summary = common.timestamp_to_datetime(httpRunner.summary, type=False)
            # print summary
            data = summary["details"][0]
            return data["records"][0]
        else:
            fact_iter(httpRunner, 1, 3, yaml_list)
    except:
        return response.RUN_CASE_FAIL

    reportName = common.get_time_stamp()
    httpRunner.gen_html_report(reportName, html_report_template=os.path.join(os.getcwd(), "httprunner", "templates",
                                                                             "extent_report_template.html"))

    # 拷贝文件到服务器
    filename = os.path.join(os.getcwd(), "reports", reportName, reportName + ".html")
    try:
        report_url = ftp_file(filename, reportName)
        res = {}
        res["report_url"] = report_url
    except Exception as err:
        logger.error("Html报告上传到服务器失败:" + err.message)
        return response.REPORT_UPLOAD_FAIL

    # 添加report表(同步执行报告)
    kwargs = {}
    kwargs["report_name"] = reportName
    kwargs["reports_url"] = res["report_url"]
    kwargs["status"] = httpRunner.summary["success"]
    kwargs["testsRun"] = httpRunner.summary["stat"]["testsRun"]
    kwargs["successes"] = httpRunner.summary["stat"]["successes"]
    kwargs["failures"] = httpRunner.summary["stat"]["failures"]
    kwargs["errors"] = httpRunner.summary["stat"]["errors"]
    kwargs["name"] = name
    kwargs["create_author"] = user
    dbUtil.add_TestReports_data(is_Async=False, **kwargs)
    res["report_status"] = kwargs["status"]
    return res


@back_async
def async_httpRunner_runner(user, yaml_list=[]):
    """
    httpRunner异步执行器
    :param path:
    :return:
    """
    kwargs = {
        "failfast": False,
    }
    httpRunner = HttpRunner(**kwargs)
    try:
        httpRunner.run(yaml_list)
    except:
        return response.RUN_CASE_FAIL

    reportName = common.get_time_stamp()
    httpRunner.gen_html_report(reportName)

    # 拷贝文件到服务器
    filename = os.path.join(os.getcwd(), "reports", reportName, reportName + ".html")
    try:
        report_url = ftp_file(filename, reportName)
    except Exception as err:
        logger.error("Html报告上传到服务器失败:" + err.message)
        return response.REPORT_UPLOAD_FAIL

    # 添加report表(异步执行报告)
    kwargs = {}
    kwargs["report_name"] = reportName
    kwargs["reports_url"] = report_url
    kwargs["status"] = httpRunner.summary["success"]
    kwargs["testsRun"] = httpRunner.summary["stat"]["testsRun"]
    kwargs["successes"] = httpRunner.summary["stat"]["successes"]
    kwargs["failures"] = httpRunner.summary["stat"]["failures"]
    kwargs["errors"] = httpRunner.summary["stat"]["errors"]
    kwargs["create_author"] = user
    dbUtil.add_TestReports_data(is_async=True, **kwargs)


@api_view(['POST'])
def run_api(request):
    """ run api by body and config
    """

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, common.get_time_stamp())

    try:
        user = request.user.username
        ids = request.data.get("index")
        env_name = request.data.get("env_name")
    except KeyError:
        return Response(response.KEY_MISS)

    msg = runner.runApi_by_single(ids, env_name, testcase_dir_path)
    res = common.get_msg(msg)
    if res != "OK":
        return Response(res)
    else:
        summary = httpRunner_runner(user, testcase_dir_path, True)
        shutil.rmtree(testcase_dir_path)
        return Response(summary)


@api_view(['POST'])
def debug_api(request):
    """ run api by body and config
    """

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, common.get_time_stamp())
    try:
        user = request.user.username
        data = request.data
        msg = runner.debugApi(testcase_dir_path, data)
    except KeyError:
        return Response(response.KEY_MISS)

    res = common.get_msg(msg)
    if res != "OK":
        return Response(res)
    else:
        summary = httpRunner_runner(user, testcase_dir_path, True)
        # shutil.rmtree(testcase_dir_path)
        if summary.get("meta_data").get("response").has_key("json") and summary.get("meta_data").get("response").get(
                "json") is not None:
            text = summary.get("meta_data").get("response").get("json")
        else:
            text = summary.get("meta_data").get("response").get("text")
        if summary["status"] =="success":
            debug_res = {
                "result": {
                    "success": True,
                    "header": summary.get("meta_data").get("response").get("headers"),
                    "response": text
                }}
        else:
            debug_res = {
                "result": {
                    "success": False,
                    "header": "",
                    "response": summary.get("attachment"),
                }}
        return Response(debug_res)


@api_view(['POST'])
def run_CaseOrSuite(request):
    """ run case or suite by body and config
    """

    # dir = os.path.abspath(os.path.dirname(os.getcwd()))
    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, common.get_time_stamp())
    try:
        user = request.user.username
        ids = request.data.get("index")
        if len(ids) == 0:
            return Response(response.RUN_CASE_NONE)
        env_name = request.data.get("env_name")
        is_async = request.data.get("is_async")
        is_async = eval(is_async)

    except KeyError:
        return Response(response.KEY_MISS)

    url = request.path
    if "case/run" in url:
        res = runner.run_by_batch(ids, env_name, testcase_dir_path, "case")
    elif "suite/run" in url:
        res = runner.run_by_batch(ids, env_name, testcase_dir_path, "suite")

    if not isinstance(res, list):
        res = common.get_msg(res)
        return Response(res)
    elif is_async:
        async_httpRunner_runner(user, yaml_list=res)
        return Response(response.RUN_ASYNC_SUCCESS)
    else:
        if len(eval(ids)) == 1 and "suite/run" in url:
            suite_obj = dbUtil.get_suite_byId(eval(ids)[0])
            res = httpRunner_runner(user, testcase_dir_path, yaml_list=res, name=suite_obj.name)
        else:
            res = httpRunner_runner(user, testcase_dir_path, yaml_list=res)
        shutil.rmtree(testcase_dir_path)
        return Response(res)
