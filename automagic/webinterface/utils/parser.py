#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2018/12/29 16:31

import logging
from webinterface.utils import dbUtil, common

logger = logging.getLogger('webinterface.views')


def case_info_logic(user, type=True, **kwargs):
    """
    用例信息逻辑处理以数据处理
    :param type: boolean: True 默认新增用例信息， False: 更新用例
    :param kwargs: dict: 用例信息
    :return: str: ok or tips
    """
    test = kwargs
    '''
        动态展示模块
    '''
    logging.info('用例原始信息: {kwargs}'.format(kwargs=kwargs))

    if test.get("name").get("case_name") is "":
        return '用例名称不可为空'
    if test.get("name").get("module") == "请选择":
        return "请选择或者添加模块"
    if test.get("name").get("project") == "请选择":
        return "请选择项目"
    if test.get("name").get("project") == "":
        return "请先添加项目"
    if test.get("name").get("module") == "":
        return "请添加模块"

    name = test.pop("name")
    test.setdefault("name", name["name"])
    test.setdefault("module", name.pop("module"))
    test.setdefault("project", name.pop("project"))
    test.setdefault("author", user)
    test.setdefault("index", name.pop("index"))

    # 处理parameters数据
    if test.has_key("parameters"):
        parameters = test.pop("parameters")
        if parameters:
            params_list = common.key_value_list("parameters", **parameters)
            if not isinstance(params_list, list):
                return params_list
            test.setdefault("parameters", params_list)
    else:
        test.setdefault("parameters", "[]")

    # 处理api数据
    cases = []
    apis = test.pop("api")
    if len(apis) > 0:
        for api in apis:
            # 处理api的request
            api_db_data = dbUtil.get_api_datails(api.get("index"))
            api_request = api.get("request")
            api_request_data = api_db_data["data"]["test"]["request"]
            if type:
                # case新增数据处理
                api["request"] = api_request_data
            else:
                # case编辑数据处理
                if len(api_request) > 0:
                    request_data = api.get("request").pop("request_data")
                    data_type = api.get("request").pop("type")
                    headers = api.get("request").pop("headers")
                    if api_request_data.has_key("json"):
                        api_request_data.pop("json")
                    elif api_request_data.has_key("data"):
                        api_request_data.pop("data")
                    api["request"] = api_request_data
                    if request_data and data_type:
                        if data_type == "json":
                            if request_data:
                                import json
                                request_data = json.loads(request_data)
                                # print request_data
                                api["request"]["json"] = request_data
                        else:
                            data_dict = common.key_value_dict("data", request_data)
                            if not isinstance(data_dict, dict) and data_dict is not None:
                                return data_dict
                            if data_dict:
                                api["request"]["data"] = data_dict
                    api["request"]["headers"] = headers
                else:
                    api["request"] = api_request_data


            # 处理api的validate
            validate = api.pop("validate")
            if validate:
                validate_list = common.key_value_list("validate", **validate)
                if not isinstance(validate_list, list):
                    return validate_list
                api.setdefault("validate", validate_list)

            # 处理api的extract
            extract = api.pop("extract")
            if extract:
                api.setdefault("extract", common.key_value_list("extract", **extract))

            # 处理api的variables
            # variables = api.pop("variables")
            # if variables:
            #     variables_list = common.key_value_list("variables", **variables)
            #     if not isinstance(variables_list, list):
            #         return variables_list
            #     api.setdefault("variables", variables_list)

            # 处理api的hooks
            # hooks = api.pop("hooks")
            # if hooks:
            #     setup_hooks_list = common.key_value_list("setup_hooks", **hooks)
            #     if not isinstance(setup_hooks_list, list):
            #         return setup_hooks_list
            #     api.get("data").setdefault("setup_hooks", setup_hooks_list)
            #
            #     teardown_hooks_list = common.key_value_list("teardown_hooks", **hooks)
            #     if not isinstance(teardown_hooks_list, list):
            #         return teardown_hooks_list
            #     api.setdefault("teardown_hooks", teardown_hooks_list)

            index = api.pop("index")
            case = {"data": {'test': api}, "index": index}
            api_name = dbUtil.get_api_datails(api_id=index)["name"]
            case["data"]["test"]["name"] = api_name
            cases.append(case)

    test.setdefault("api", cases)
    logger.info("case_finish:{}".format(kwargs))
    return dbUtil.add_case_data(type, **kwargs)


def api_info_logic(user, type=True, **kwargs):
    """
    api信息逻辑处理以数据处理
    :param type: boolean: True 默认新增api信息， False: 更新api
    :param kwargs: dict: api信息
    :return: str: ok or tips
    """
    test = kwargs
    '''
        动态展示模块
    '''
    logging.info('api原始信息: {kwargs}'.format(kwargs=kwargs))
    if test.get("name").get("name") is "":
        return 'api名称不可为空'
    if test.get("name").get("module") == "请选择":
        return "请选择或者添加模块"
    if test.get("name").get("project") == "请选择":
        return "请选择项目"
    if test.get("name").get("project") == "":
        return "请先添加项目"
    if test.get("name").get("module") == "":
        return "请添加模块"

    name = test.pop("name")
    test.setdefault("name", name["name"])
    test.setdefault("module", name.pop("module"))
    test.setdefault("project", name.pop("project"))
    test.setdefault("author", user)
    test.setdefault("index", name.pop("index"))

    # 处理api的request
    request_data = test.get("request").pop("request_data")
    data_type = test.get("request").pop("type")
    if request_data and data_type:
        if data_type == "json":
            import json
            if len(request_data) > 0:
                request_data = json.loads(request_data)
            test.get("request").setdefault(data_type, request_data)
        else:
            data_dict = common.key_value_dict("data", request_data)
            if not isinstance(data_dict, dict):
                return data_dict
            test.get("request").setdefault(data_type, data_dict)
    else:
        if data_type == "json":
            test.get("request").setdefault(data_type, "")
    headers = test.get("request").pop("headers")
    if headers:
        test.get("request").setdefault("headers", common.key_value_dict("headers", headers))

    request = test.pop("request")
    # 处理url（https://resapi.wondershare.com/api/v1.1/configs  ---------> /api/v1.1/configs）
    url = request["url"]
    test.setdefault("url", url)
    if "http" in url:
        hostName = url.split("/")[2]
        logger.info("url为：{}，hostName为：{}".format(url, hostName))
        new_url = url.split(hostName)[1]
        request["url"] = new_url
    else:
        return "url地址格式输入错误：{}（缺少http或https）".format(url)
    test["request"] = {'test': {'request': request}}
    test["request"]["test"]["name"] = name.pop("name")
    logger.info("api_finish:{}".format(kwargs))

    return dbUtil.add_api_data(type, **kwargs)


##add by yansl@wondershare.cn
# ENV 配置相关api
def env_info_logic(type=True, **kwargs):
    """
    ENV 配置处理
    :param type: boolean: True 默认新增， False: 更新
    :param kwargs: dict: ENV信息
    :return: str: ok or tips
    """
    test = kwargs
    '''
        动态展示模块
    '''
    logging.info('用例原始信息: {kwargs}'.format(kwargs=kwargs))
    if test.get("name").get("case_name") is "":
        return '用例名称不可为空'
    if test.get("name").get("module") == "请选择":
        return "请选择或者添加模块"
    if test.get("name").get("project") == "请选择":
        return "请选择项目"
    if test.get("name").get("project") == "":
        return "请先添加项目"
    if test.get("name").get("module") == "":
        return "请添加模块"

    name = test.pop("name")
    test.setdefault("name", name["name"])
    test.setdefault("module", name.pop("module"))
    test.setdefault("project", name.pop("project"))
    test.setdefault("author", name.pop("author"))
    test.setdefault("index", name.pop("index"))
    test.setdefault("api", name.pop("api"))

    # print("test2:{}".format(test))
    test.setdefault("test", {})
    validate = test.pop("validate")
    if validate:
        validate_list = common.key_value_list("validate", **validate)
        if not isinstance(validate_list, list):
            return validate_list
        test.get("test").setdefault("validate", validate_list)

    extract = test.pop("extract")
    if extract:
        test.get("test").setdefault("extract", common.key_value_list("extract", **extract))

    variables = test.pop("variables")
    if variables:
        variables_list = common.key_value_list("variables", **variables)
        if not isinstance(variables_list, list):
            return variables_list
        test.get("test").setdefault("variables", variables_list)

    # parameters = test.pop("parameters")
    # if parameters:
    #     params_list = common.key_value_list("parameters", **parameters)
    #     if not isinstance(params_list, list):
    #         return params_list
    #     test.setdefault("parameters", params_list)

    hooks = test.pop("hooks")
    if hooks:
        setup_hooks_list = common.key_value_list("setup_hooks", **hooks)
        if not isinstance(setup_hooks_list, list):
            return setup_hooks_list
        test.get("test").setdefault("setup_hooks", setup_hooks_list)

        teardown_hooks_list = common.key_value_list("teardown_hooks", **hooks)
        if not isinstance(teardown_hooks_list, list):
            return teardown_hooks_list
        test.get("test").setdefault("teardown_hooks", teardown_hooks_list)

    print("test_finish:{}".format(kwargs))
    return dbUtil.add_case_data(type, **kwargs)


def env_info_logic(params, type=True):
    """
    env信息逻辑处理以数据处理
    :param type: boolean: True 默认新增env信息， False: 更新env
    :param kwargs: dict: env信息
    :return: str: ok or tips
    """

    # print("test:{}".format(test))
    '''
        动态展示模块
    '''
    logging.info('env原始信息: {params}'.format(params=params))
    if params.get("env_name") is "":
        return 'env名称不可为空'
    if type:
        return dbUtil.add_env_data(params)
    else:
        return dbUtil.edit_env_data(params)


def del_env_data(env_id, author):
    return dbUtil.del_env_data(env_id, author)


def del_host_data(id, update_author):
    return dbUtil.del_host_data(id, update_author)


def del_host_by_envid(env_id, author):
    return dbUtil.del_host_by_envid(env_id, author)


def host_info_logic(kwargs, type=True, ):
    """
    host信息逻辑处理以数据处理
    :param type: boolean: True 默认新增host信息， False: 更新host
    :param kwargs: dict: host信息
    :return: str: ok or tips
    """
    params = kwargs

    logging.info('host_info原始信息: {kwargs}'.format(kwargs=kwargs))
    if params.get("base_url") is "":
        return 'base_url不可为空'
    if params.get("host") is "":
        return "host不可为空"

    if type:
        return dbUtil.add_host_data(kwargs)
    else:
        return dbUtil.edit_host_data(kwargs)
