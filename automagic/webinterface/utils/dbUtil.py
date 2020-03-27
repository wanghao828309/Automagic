#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/4 16:59
import logging
from webinterface.models import API, CaseInfo, APIandCaseInfo, Env, Host, DebugTalk, FileBinary, TestReports,Suite
from autoplat.models import Project, Module, UserandProduct
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

logger = logging.getLogger('webinterface.views')


##############################################################################################
#                                                                                             #
#                                 FileBinary数据库操作                                           #
#                                                                                             #
##############################################################################################
def get_fileBody_byName(name):
    file_body = FileBinary.objects.filter(name=name).values('body')
    return file_body


##############################################################################################
#                                                                                             #
#                                 product数据库操作                                           #
#                                                                                             #
##############################################################################################
def get_product_byUser(name):
    productid = UserandProduct.objects.filter(username__username=name).values('productname')
    return productid


def get_productObj_byUser(name):
    product = UserandProduct.objects.filter(username__username=name)
    return product


def get_project_byProduct(product):
    projectid = Project.objects.filter(productid__in=product).values('id')
    return projectid


def get_product_byProject(projectName):
    product = Project.objects.get(name=projectName)
    return product


##############################################################################################
#                                                                                             #
#                                 api数据库操作                                               #
#                                                                                             #
##############################################################################################
def add_api_data(type, **kwargs):
    """
    api信息落地
    :param type: boolean: true: 添加新api， false: 更新api
    :param kwargs: dict
    :return: ok or tips
    """
    test = kwargs
    API_opt = API.objects
    name = test.get("name")
    moduleName = test.get("module")
    projectName = test.get("project")

    if Module.objects.filter(name=moduleName).count() == 0:
        return "模块不存在"
    else:
        module = Module.objects.get(name=moduleName, projectid__name=projectName)
        test.pop("module")
        test.setdefault("module", module)

    if Project.objects.filter(name=projectName).count() == 0:
        return "工程不存在"
    else:
        project = Project.objects.get(name=projectName)
        test.pop("project")
        test.setdefault("project", project)

    if type:
        logger.info("添加的API：{}".format(test))
        if API_opt.filter(name=name, delStatus=0).count() > 0:
            return 'API名称重复'
        else:
            API_opt.insert_API(**test)
            logger.info("{name}:API添加成功: {test}".format(name=name, test=test))
    else:
        logger.info("更新的API：{}".format(test))
        try:
            index = test.get("index")
            if len(index) > 0:
                if API_opt.get_by_id(index).name != name and API_opt.filter(name=name, delStatus=0).count() > 0:
                    return 'API名称重复'
                else:
                    API_opt.update_API(**test)
                    logger.info("{name}:API更新成功: {test}".format(name=name, test=test))
            else:
                return "API的id为空"
        except ObjectDoesNotExist:
            return "API不存在"

    return "ok"


def del_single_api_data(user, **kwargs):
    """
    删除api
    :param kwargs:
    :return:
    """

    index = kwargs.get('index')[0]
    author = user
    api_obj = API.objects
    api_obj.delete_API(index, author)

    # if len(index_list) > 0:
    #     indexs = eval(index_list)
    #     author = user
    #     api_obj = API.objects
    #     for index in indexs:
    #         api_obj.delete_API(index, author)
    return "ok"


def get_api_datails(api_id):
    """
    获取id=api_id的api详情
    :param case_id:
    :return:
    """
    try:
        api_info = API.objects.get_by_id(api_id)
        product = get_product_byProject(api_info.project.name)
        # print product
    except ObjectDoesNotExist:
        return "id为{}:api不存在".format(api_id)
    data = eval(api_info.data)
    # modify by yansl 修改获取逻辑
    res = {
        'name': api_info.name,
        'url': api_info.url,
        'method': api_info.method,
        "product": product.productid.name,
        'project': api_info.project.name,
        'module': api_info.module.name,
        'data': data,
    }
    return res


##############################################################################################
#                                                                                             #
#                                 case数据库操作                                              #
#                                                                                             #
##############################################################################################
@transaction.atomic
def add_case_data(type, **kwargs):
    """
    case信息落地
    :param type: boolean: true: 添加新case， false: 更新case
    :param kwargs: dict
    :return: ok or tips
    """
    test = kwargs
    CaseInfo_opt = CaseInfo.objects
    name = test.get("name")
    author = test.get("author")
    moduleName = test.get("module")
    projectName = test.get("project")
    apis = test.get("api")
    index = test.get("index")

    if Module.objects.filter(name=moduleName).count() == 0:
        return "模块不存在"
    else:
        module = Module.objects.get(name=moduleName, projectid__name=projectName)
        test.pop("module")
        test.setdefault("module", module)

    if Project.objects.filter(name=projectName).count() == 0:
        return "工程不存在"
    else:
        project = Project.objects.get(name=projectName)
        test.pop("project")
        test.setdefault("project", project)

    if type:
        # case表插入记录
        logger.info("添加的case：{}".format(test))
        if CaseInfo_opt.filter(name=name, delStatus=0).count() > 0:
            return 'case名称重复'
        else:
            CaseInfo_opt.insert_CaseInfo(**test)
    else:
        # case表更新记录
        logger.info("更新的case：{}".format(test))
        try:
            if len(index) > 0:
                if CaseInfo_opt.get_by_id(index).name != name and CaseInfo_opt.filter(name=name,
                                                                                      delStatus=0).count() > 0:
                    return 'case名称重复'
                else:
                    CaseInfo_opt.update_CaseInfo(**test)
                    # 获取当前case = index的全部绑定关系
                    apiandcases_list = []
                    apiandcases_sets = CaseInfo_opt.get_by_id(index).apiandcaseinfo_set.filter(delStatus=0)
                    if len(apiandcases_sets) > 0:
                        for apiandcases_obj in apiandcases_sets:
                            apiandcases_list.append(apiandcases_obj)
                    logger.info("caseid为：{}的全部绑定关系集合是:".format(index))
                    logger.info(apiandcases_list)
            else:
                return "case的id为空"
        except ObjectDoesNotExist:
            return "case不存在"

    APIandCase_opt = APIandCaseInfo.objects
    # 判断更新时，删除原有绑定关系
    if not type:
        logger.info("caseid为：{}的需要删除的绑定关系集合是：".format(index))
        logger.info(apiandcases_list)
        if len(apiandcases_list) > 0:
            for apiandcases_obj in apiandcases_list:
                APIandCase_opt.delete_APIandCase(apiandcases_obj.id, author)

    if len(apis) > 0:
        API_opt = API.objects
        case_obj = CaseInfo_opt.get(name=name, delStatus=0)
        try:
            for sortId, api in enumerate(apis):
                api_index = api["index"]
                logger.info("接口指定的api的id是：{}".format(api_index))
                if type:
                    # 绑定新关系表(增加逻辑)
                    api_obj = API_opt.get_by_id(id=api_index)
                    APIandCase_opt.insert_APIandCase(case_obj, api_obj, api["data"], author, sortId)
                    logger.info("{name}:case添加成功".format(name=name))
                else:
                    # 绑定新关系表
                    api_obj = API_opt.get(id=api_index, delStatus=0)
                    APIandCase_opt.insert_APIandCase(case_obj, api_obj, api["data"], author, sortId)
            logger.info("{name}:case更新成功".format(name=name))

            #         # 更新关系表(更新逻辑)
            #         apiandcases_sets = CaseInfo_opt.get_by_id(index).apiandcaseinfo_set.filter(delStatus=0,
            #                                                                                    caseInfo=index,
            #                                                                                    api=api_index)
            #
            #         print apiandcases_sets
            #         if len(apiandcases_sets) > 0:
            #             # 更新绑定关系
            #             for apiandcases_obj in apiandcases_sets:
            #                 APIandCase_opt.update_APIandCase_byId(apiandcases_obj.id, author, api["data"], sortId)
            #                 print apiandcases_list
            #                 print apiandcases_obj
            #                 list_id = apiandcases_list.index(apiandcases_obj)
            #                 del apiandcases_list[list_id]
            #                 # if apiandcases_obj in apiandcases_list:
            #                 #     apiandcases_list.remove(apiandcases_obj)
            #         else:
            #             # 绑定新关系表
            #             api_obj = API_opt.get(id=api_index, delStatus=0)
            #             APIandCase_opt.insert_APIandCase(case_obj, api_obj, api["data"], author, sortId)
            #         # # 更新api
            #         # API_opt.update_API_data(api_index, api["request"], author)
            #
            # # 删除原有绑定关系
            # if not type:
            #     logger.info("caseid为：{}的需要删除的绑定关系集合是：".format(index))
            #     logger.info(apiandcases_list)
            #     if len(apiandcases_list) > 0:
            #         for apiandcases_obj in apiandcases_list:
            #             APIandCase_opt.delete_APIandCase(apiandcases_obj.id, author)


        except ObjectDoesNotExist:
            return "id为{}:api不存在".format(api_index)

    return "ok"


@transaction.atomic
def del_case_data(kwargs, user):
    """
    删除case
    :param kwargs:
    :return:
    """
    id = kwargs.get('index')
    author = user
    apiandcase = APIandCaseInfo.objects
    case_obj = CaseInfo.objects
    apiandcase_set = case_obj.get_by_id(id).apiandcaseinfo_set.filter(delStatus=0)
    for apiandcase_obj in apiandcase_set:
        apiandcase.delete_APIandCase(apiandcase_obj.id, author)  # 删除绑定关系
    case_obj.delete_case(id, author)  # 删除用例

    # if len(ids) > 0:
    #     ids = eval(ids)
    #     author = user
    #     for id in ids:
    #         apiandcase = APIandCaseInfo.objects
    #         case_obj = CaseInfo.objects
    #         apiandcase_set = case_obj.get_by_id(id).apiandcaseinfo_set.filter(delStatus=0)
    #         for apiandcase_obj in apiandcase_set:
    #             apiandcase.delete_APIandCase(apiandcase_obj.id, author)  # 删除绑定关系
    #         case_obj.delete_case(id, author)  # 删除用例

    return "ok"


def get_case_datails(case_id):
    """
    获取id=case_id的case详情
    :param case_id:
    :return:
    """
    case_obj = CaseInfo.objects
    case_info = case_obj.get_by_id(id=case_id)
    apiandcases = case_info.apiandcaseinfo_set.filter(delStatus=0)
    data = eval(case_info.data)
    apis = []
    for a in apiandcases:
        try:
            # 获取关联api信息详情
            api_info = API.objects.get_by_id(a.api.id)
            api_dict = {}
            api_dict['id'] = api_info.id
            api_dict['name'] = api_info.name
            api_dict['url'] = api_info.url
            api_dict['method'] = api_info.method
            api_dict['request'] = eval(api_info.data)
            api_dict['data'] = eval(a.data)
            apis.append(api_dict)
        except ObjectDoesNotExist:
            return "id为{}:api不存在".format(a.api.id)

    res = {
        'apis': apis,  # 关联的api信息
        'name': case_info.name,
    }
    return res


##############################################################################################
#                                                                                             #
#                                 debugTalk数据库操作                                         #
#                                                                                             #
##############################################################################################
def update_debugTalk_datails(**kwargs):
    """
    更新debugtalk表的code
    :return:
    """
    try:
        author = kwargs.get("author")
        code = kwargs.get("code")
        debugTalk_obj = DebugTalk.objects
        debugTalk_obj.update_debugTalk("debugtalk", author, code)
    except ObjectDoesNotExist:
        return "名称为:debugtalk数据不存在"
    except:
        return "请求参数错误"

    return "ok"


def get_debugTalk_datails():
    """
    获取debugtalk表的code
    :return:
    """
    debugTalk_obj = DebugTalk.objects
    code = debugTalk_obj.update_debugTalk("debugtalk").code
    res = {"code": code}
    return res


def get_case_datails(case_id):
    """
    获取id=case_id的case详情
    :param case_id:
    :return:
    """
    case_obj = CaseInfo.objects
    case_info = case_obj.get_by_id(id=case_id)
    apiandcases = case_info.apiandcaseinfo_set.filter(delStatus=0).order_by("sort_by")
    product = get_product_byProject(case_info.project.name)
    data = eval(case_info.data)
    apis = []
    for a in apiandcases:
        try:
            # 获取关联api信息详情
            api_info = API.objects.get_by_id(a.api.id)
            api_dict = {}
            api_dict['id'] = api_info.id
            api_dict['name'] = api_info.name
            api_dict['url'] = api_info.url
            api_dict['method'] = api_info.method
            api_dict['data'] = eval(a.data)
            apis.append(api_dict)
        except ObjectDoesNotExist:
            return "id为{}:api不存在".format(a.api.id)

    res = {
        'apis': apis,  # 关联的api信息
        'name': case_info.name,
        "data": data,
        "product": product.productid.name,
        "project": case_info.project.name,
        "module": case_info.module.name
    }
    return res


##############################################################################################
#                                                                                             #
#                                 reports数据库操作                                           #
#                                                                                             #
##############################################################################################
def add_TestReports_data(is_Async=True, **kwargs):
    """
    插入report表
    :param kwargs:
    """
    testReports_obj = TestReports.objects
    if is_Async:
        testReports_obj.insert_Reports_Async(**kwargs)
    else:
        testReports_obj.insert_Reports_noAsync(**kwargs)


def get_report_byId(id):
    report = TestReports.objects.get_by_id(id=id)
    return report


##############################################################################################
#                                                                                             #
#                                 debugTalk数据库操作                                         #
#                                                                                             #
##############################################################################################
def update_debugTalk_datails(code, user):
    """
    更新debugtalk表的code
    :return:
    """
    try:
        author = user
        debugTalk_obj = DebugTalk.objects
        debugTalk_obj.update_debugTalk("debugtalk", author, code)
    except ObjectDoesNotExist:
        return "名称为:debugtalk数据不存在"
    except:
        return "请求参数错误"

    return "ok"


def get_debugTalk_datails():
    """
    获取debugtalk表的code
    :return:
    """
    code = DebugTalk.objects.values('id', 'code').get(name="debugtalk")
    return code


##############################################################################################
#                                                                                             #
#                                 env数据库操作                                              #
#                                                                                             #
##############################################################################################
def add_env_data(kwargs):
    """
    env信息落地
    :param type: boolean: true: 添加新env， false: 更新env
    :param kwargs: dict
    :return: ok or tips
    """
    env = kwargs
    Env_opt = Env.objects
    name = env.get("env_name")
    create_author = env.get("create_author")
    update_author = env.get("update_author")

    logger.info("添加的env：{}".format(env))
    if Env_opt.filter(env_name=name, delStatus=0).count() > 0:
        return 'ENV名称重复'
    else:
        Env_opt.insert_Env(name, env.get("simple_desc"), create_author, update_author)
        # logger.info("{name}:ENV添加成功: {env}".format(name=name, env=env))
        return "ok"


def edit_env_data(kwargs):
    env_info = kwargs
    env_id = kwargs.get("env_id")
    name = env_info.get("env_name")
    update_author = env_info.get("update_author")
    simple_desc = " "
    Env_opt = Env.objects
    logger.info("更新的env：{}".format(env_info))
    try:
        if Env_opt.get_by_id(env_id).env_name != name and Env_opt.filter(env_name=name, delStatus=0
                                                                         ).count() > 0:
            return 'ENV名称重复'
        else:
            Env_opt.update_env(env_id, name, update_author)
            # logger.info("{name}:ENV更新成功: {env}".format(name=name, env=env))

    except ObjectDoesNotExist:
        return "ENV不存在"
    return "ok"


def del_env_data(env_id, author):
    Env_opt = Env.objects

    Env_opt.delete_Env(env_id, author)

    return "ok"


def add_host_data(kwargs):
    """
    host信息落地
    :param type: boolean: true: 添加新host， false: 更新host
    :param kwargs: dict
    :return: ok or tips
    """
    host = kwargs

    base_url = host.get("base_url")
    host_domain = host.get("host")
    env_id = host.get("env_id")
    if base_url is "":
        return "url不能为空"
    if host_domain is "":
        return "host不能为空"
    if env_id is "":
        return "host所属env不能为空"
    if Env.objects.filter(id=env_id).count() == 0:
        return "环境不存在"

    if Host.objects.filter(base_url=base_url, delStatus=0, env_id=env_id).count() > 0:
        return "已存在同样的host，不可重复添加"

    logger.info("添加的host：{}".format(host))
    return Host.objects.insert_Host(host)


def edit_host_data(kwargs):
    host = kwargs

    logger.info("更新的host：{}".format(host))
    try:
        host_id = host.get("hostid")
        if len(host_id) > 0:
            if Host.objects.filter(id=host_id, delStatus=0).count() <= 0:
                return "host不存在"
            Host.objects.update_Host(host)
            logger.info("HOST更新成功: {host}".format(host=host))
        else:
            return "host的id为空"
    except ObjectDoesNotExist:
        return "HOST不存在"

    return "ok"


def del_host_data(id, update_author):
    if Host.objects.filter(id=id, delStatus=0).count() <= 0:
        return "host数据不存在"

    Host.objects.del_Host(id, update_author)
    return "ok"


def del_host_by_envid(env_id, author):
    Host_opt = Host.objects
    Host_opt.delete_by_env(env_id, author)
    return "ok"


##############################################################################################
#                                                                                             #
#                                 Suite数据库操作                                           #
#                                                                                             #
##############################################################################################
def get_suite_byId(id):
    suite = Suite.objects.get_by_id(id=id)
    return suite