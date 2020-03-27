#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/8 14:59
import os, logging
from webinterface.models import API, CaseInfo, Env, DebugTalk, Suite
from webinterface.utils import common
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('webinterface.views')


def create_init_file(path):
    """
    生成__init__.py文件
    :param path: 生成路径
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    common.dump_python_file(os.path.join(path, '__init__.py'), u"")


def create_debugtalk_file(path):
    """
    生成debugtalk.py文件
    :param path: 生成路径
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        debugtalk = DebugTalk.objects.get(name="debugtalk").code
    except ObjectDoesNotExist:
        return "miss debugtalk"
    common.dump_python_file(os.path.join(path, 'debugtalk.py'), debugtalk)
    common.dump_python_file(os.path.join(path, '__init__.py'), u"")


def get_host(envName, api_url):
    """
    根据env表name关联host表的host（1对多关系）
    :param envName:
    :param api_url:
    :return:
    """
    env = Env.objects.get_by_name(envName)
    host_list = env.host_set.filter(delStatus=0)
    if len(host_list) > 0:
        for host in host_list:
            if host.base_url in api_url:
                return host

    # env_name = env.env_name


def runApi_by_single(index, env_name, path):
    """
    运行单个api
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    try:
        api = API.objects.get_by_id(id=index)
    except ObjectDoesNotExist:
        return '未查询到该API'
    try:
        host = get_host(env_name, api.url)
        if host is None:
            return "请先在环境里配置host"
        else:
            base_host = host.host
            base_url = host.base_url  # effects.wondershare.com
            base_urls = api.url.split("//")
            base_url_new = base_urls[0] + "//" + base_host  # https://10.10.18.101
            host_new = base_url  # effects.wondershare.com
    except ObjectDoesNotExist:
        return "指定的环境不存在"

    config = {
        'config': {
            'request': {
                'verify': False,
                'base_url': base_url_new,
                "headers": {
                    "Host": host_new,
                }
            }
        }
    }
    testapi_list = []

    data = eval(api.data)
    if data.get("test").get("request").has_key("headers"):
        headers = data.get("test").get("request").get("headers")
        if headers.has_key("Host") and headers.get("Host") == "None":
            config.get("config").get("request").pop("headers")
            headers.pop("Host")

    testapi_list.append(config)
    testapi_list.append(data)
    name = api.name
    project = api.project.id
    module = api.module.id
    config['config']['name'] = name
    # 生成__init__.py文件
    create_init_file(path)
    testcase_dir_path = os.path.join(path, str(project))

    # 生成debugtalk.py文件
    create_debugtalk_file(testcase_dir_path)
    # 生成yaml文件
    testcase_dir_path = os.path.join(testcase_dir_path, str(module))
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    logger.info("运行api的json为：{}".format(testapi_list))
    common.dump_yaml_file(os.path.join(testcase_dir_path, name + '.yml'), testapi_list)
    return "ok"


def runCase_by_single(index, env_name, path):
    """
    运行单个case
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """

    # 配置config
    try:
        case_obj = CaseInfo.objects.get_by_id(id=index)
    except ObjectDoesNotExist:
        return '未查询到case的id为：{} 的case'.format(index)
    config = {
        'config': {
        }
    }
    testapi_list = []
    testapi_list.append(config)
    name = case_obj.name
    project = case_obj.project.id
    module = case_obj.module.id
    # 获取parameters
    if len(case_obj.data) > 0:
        parameters = eval(case_obj.data)
        config['config']['parameters'] = parameters
    config['config']['name'] = name
    # 生成__init__.py文件
    # print "filePath:" + path
    create_init_file(path)
    testcase_dir_path = os.path.join(path, str(project))

    # 组装Test通过api与apiandcaseinfo表
    apiandcases_set = case_obj.apiandcaseinfo_set.filter(delStatus=0).order_by("sort_by")
    api = API.objects
    for apiandcases_obj in apiandcases_set:
        try:
            API_obj = api.get_by_id(id=apiandcases_obj.api.id)
        except ObjectDoesNotExist:
            return '未查询到API的id为：{} 的API'.format(apiandcases_obj.api.id)
        # data = eval(API_obj.data)
        parms = eval(apiandcases_obj.data)

        # 解析host与url
        try:
            host = get_host(env_name, API_obj.url)
            if host is None:
                return "请先名称为：{}的case，在环境里配置host".format(name)
            else:
                base_host = host.host  # 10.10.18.101
                base_url = host.base_url  # effects.wondershare.com
                base_urls = API_obj.url.split("//")
                base_url_new = base_urls[0] + "//" + base_host  # https://10.10.18.101
                host_new = base_url  # effects.wondershare.com
                if parms.get("test").get("request").has_key("url"):
                    test_url = parms.get("test").get("request").get("url")  # /api/v1.1/configs
                else:
                    return "case名称为：{}，request里缺少url".format(name)
                url = base_url_new + test_url  # https://47.254.68.213/api/v1.1/configs
                logger.info("运行case的url为：{}".format(url))
                request = parms.get("test").get("request")
                request["url"] = url
                request.setdefault("verify", False)
                if request.has_key("headers"):
                    if request.get("headers").has_key("Host") and request.get("headers").get("Host") == "None":
                        request.get("headers").pop("Host")
                    else:
                        request.get("headers").setdefault("Host", host_new)
                else:
                    request.setdefault("headers", {})
                    request.get("headers").setdefault("Host", host_new)
        except ObjectDoesNotExist:
            return "指定的环境不存在"

        # 删除validate选项下的type
        if parms["test"].has_key("validate"):
            for validate in parms["test"]["validate"]:
                if validate.has_key("type"):
                    validate.pop("type")

        testapi_list.append(parms)

    if len(apiandcases_set) > 0:
        # 生成debugtalk.py文件
        create_debugtalk_file(testcase_dir_path)
        # 生成yaml文件
        testcase_dir_path = os.path.join(testcase_dir_path, str(module))
        if not os.path.exists(testcase_dir_path):
            os.makedirs(testcase_dir_path)
        logger.info("运行case的json为：{}".format(testapi_list))
        yaml_path = os.path.join(testcase_dir_path, name + '.yml')
        logger.info("生成case的yaml路径为：{}".format(yaml_path))
        common.dump_yaml_file(yaml_path, testapi_list)
        return ("ok", yaml_path)
    else:
        return "请case名称为：{}，先绑定api".format(name)


def runSuite_by_single(index, env_name, path):
    """
    运行单个suite
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    try:
        suite_obj = Suite.objects.get_by_id(id=index)
    except ObjectDoesNotExist:
        return '未查询到该Suite'

    caseandsuite_set = suite_obj.caseandsuite_set.filter(delStatus=0).order_by("sort_by")
    if len(caseandsuite_set) > 0:
        case_list = []
        for caseandsuite_obj in caseandsuite_set:
            # print caseandsuite_obj.case.id
            res = runCase_by_single(caseandsuite_obj.case.id, env_name, path)
            if not isinstance(res, tuple):
                return res
            else:
                case_list.append(res[1])
        return case_list


def run_by_batch(test_list, env_name, path, type, mode=False):
    """
    批量运行
    :param test_list:
    :param env_name:
    :param path:
    :param mode:
    """
    ids = eval(test_list)
    if not isinstance(ids, list):
        return "index的参数类似错误，应该为list"

    yaml_list = []
    for index in ids:
        if type == "case":
            res = runCase_by_single(index, env_name, path)
        elif type == "suite":
            res = runSuite_by_single(index, env_name, path)

        if not isinstance(res, (tuple, list)):
            return res
        elif type == "case":
            yaml_list.append(res[1])
        else:
            yaml_list.extend(res)

    logger.info(yaml_list)
    return yaml_list


def debugApi(path, data):
    """
    调试单个api
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    api_url = data.pop("url")
    env_name = data.pop("env_name")
    method = data.pop("method")
    headers = data.pop("headers")
    if len(headers) > 0:
        headers = common.key_value_dict_new("headers", headers)

    type = data.pop("type")
    if type == "json":
        import json
        request_data = data.pop("request_data")
        if len(request_data) > 0:
            request_data = json.loads(request_data)
    else:
        request_data = common.key_value_dict_new("data", data.pop("request_data"))

    try:
        host = get_host(env_name, api_url)
        if host is None:
            return "请先在环境里配置host"
        else:
            base_host = host.host
            base_url = host.base_url  # effects.wondershare.com
            base_urls = api_url.split("//")
            base_url_new = base_urls[0] + "//" + base_host  # https://10.10.18.101
            host_new = base_url  # effects.wondershare.com
    except ObjectDoesNotExist:
        return "指定的环境不存在"

    if "http" in api_url:
        hostName = api_url.split("/")[2]
        new_url = api_url.split(hostName)[1]
        api_url = new_url
    else:
        return "url地址格式输入错误：{}（缺少http或https）".format(api_url)

    if headers.has_key("Host") and headers.get("Host") == "None":
        headers.pop("Host")
        api_json = [
            {
                'config': {
                    'request': {
                        "base_url": base_url_new,
                        'verify': False,
                    }
                }
            },
            {
                "test": {
                    "request": {
                        "url": api_url,
                        "headers": headers,
                        "{}".format(type): request_data,
                        "method": method
                    },
                    "name": "api_debug"
                }
            }
        ]
    else:
        api_json = [
            {
                'config': {
                    'request': {
                        "base_url": base_url_new,
                        'verify': False,
                        "headers": {
                            "Host": host_new,
                        }
                    }
                }
            },
            {
                "test": {
                    "request": {
                        "url": api_url,
                        "headers": headers,
                        "{}".format(type): request_data,
                        "method": method
                    },
                    "name": "api_debug"
                }
            }
        ]

    # 生成__init__.py文件
    create_init_file(path)
    # 生成debugtalk.py文件
    testcase_dir_path = os.path.join(path, "debug")
    create_debugtalk_file(testcase_dir_path)
    logger.info("运行api的json为：{}".format(api_json))
    # 生成yaml文件
    common.dump_yaml_file(os.path.join(testcase_dir_path, 'api_debug.yml'), api_json)
    return "ok"
