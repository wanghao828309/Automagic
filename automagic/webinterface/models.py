#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/4 16:59

from __future__ import unicode_literals

from autoplat.models import *
from webinterface import managers


# Create your models here.

class BaseTable(models.Model):
    """
    公共字段列
    """

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

    create_author = models.CharField('编写人员', max_length=20, null=False)
    update_author = models.CharField('更新人员', max_length=20, null=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=False)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=False)
    delStatus = models.BooleanField('删除状态', default=False)


class FileBinary(models.Model):
    """
    二进制文件流
    """

    class Meta:
        verbose_name = "二进制文件"
        db_table = "FileBinary"

    name = models.CharField("文件名称", unique=True, null=False, max_length=100)
    size = models.CharField("大小", null=False, max_length=30)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)


class CaseInfo(BaseTable):
    class Meta:
        verbose_name = '用例信息'
        db_table = 'webinterface_CaseInfo'

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField('用例/配置名称', max_length=50, null=False)
    data = models.TextField("主体信息", null=False, default="[]")
    objects = managers.CaseInfoManager()


class API(BaseTable):
    class Meta:
        verbose_name = "接口信息"
        db_table = "webinterface_API"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("接口名称", null=False, max_length=100)
    url = models.CharField("请求地址", null=False, max_length=100)
    method = models.CharField("请求方式", null=False, max_length=10)
    data = models.TextField("主体信息", null=False)
    objects = managers.APIManager()


class APIandCaseInfo(BaseTable):
    class Meta:
        verbose_name = '用例与API关联表'
        db_table = 'webinterface_APIandCaseInfo'

    caseInfo = models.ForeignKey(CaseInfo, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    data = models.TextField("主体信息", null=False)
    sort_by = models.CharField('排列顺序', max_length=10, null=False, default=0)
    objects = managers.APIandCaseManager()


class Env(BaseTable):
    class Meta:
        verbose_name = '环境管理'
        db_table = 'webinterface_Env'

    env_name = models.CharField('环境名称', max_length=40, null=False)
    simple_desc = models.CharField('环境描述', max_length=50, null=False)
    objects = managers.EnvInfoManager()


class Host(BaseTable):
    class Meta:
        verbose_name = 'Host管理'
        db_table = 'webinterface_Host'

    env = models.ForeignKey(Env, on_delete=models.CASCADE)
    base_url = models.CharField('host域名', max_length=40, null=False)
    host = models.CharField('host对应服务器IP', max_length=40, null=False)
    simple_desc = models.CharField('host描述', max_length=50)
    objects = managers.HostManager()


class DebugTalk(BaseTable):
    class Meta:
        verbose_name = '驱动py文件'
        db_table = 'webinterface_DebugTalk'

    name = models.CharField("python文件名称", null=False, max_length=100, unique=True)
    code = models.TextField("python代码", default="# write you code", null=False)
    objects = managers.DebugTalkManager()


class Suite(BaseTable):
    class Meta:
        verbose_name = '测试套件'
        db_table = 'webinterface_Suite'

    name = models.CharField('名称', max_length=50, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='suite_project')
    objects = managers.SuiteManager()


class CaseandSuite(BaseTable):
    class Meta:
        verbose_name = '测试套件与测试用例关联'
        db_table = 'webinterface_CaseandSuite'

    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    case = models.ForeignKey(CaseInfo, on_delete=models.CASCADE)
    sort_by = models.CharField('排列顺序', max_length=10, null=False)


class TestReports(BaseTable):
    class Meta:
        verbose_name = "测试报告"
        db_table = 'webinterface_Reports'

    name = models.CharField(max_length=100, null=False)
    report_name = models.CharField(max_length=40, null=False)
    reports_url = models.CharField(max_length=100, null=False)
    status = models.BooleanField('是否成功', null=False)
    testsRun = models.IntegerField(null=True, blank=True)
    successes = models.IntegerField(null=True, blank=True)
    failures = models.IntegerField(null=True, blank=True)
    errors = models.IntegerField(null=True, blank=True)
    is_async = models.BooleanField('是否异步', null=False, default=False)
    objects = managers.TestReportsManager()
