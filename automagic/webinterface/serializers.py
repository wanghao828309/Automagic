# -*- coding:utf-8 -*-
import json
import demjson

from rest_framework import serializers
from webinterface import models


class APISerializer(serializers.ModelSerializer):
    """
    API序列化
    """
    data = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source="project.name")
    mudule_name = serializers.CharField(source="module.name")

    class Meta:
        model = models.API
        fields = ['id', 'project_name', 'mudule_name', 'name', 'url', 'method', 'data',
                  "create_time", "update_time", "create_author", "update_author"]

    def get_data(self, obj):
        return demjson.encode(obj.data)


class CaseSerializer(serializers.ModelSerializer):
    """
    Case序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project_name = serializers.CharField(source="project.name")
    mudule_name = serializers.CharField(source="module.name")

    class Meta:
        model = models.CaseInfo
        fields = ['id', 'project_name', 'mudule_name', 'name', 'create_author', 'update_author',
                  "create_time", "update_time", "create_author", "update_author"]


class CaseAndApiSerializer(serializers.ModelSerializer):
    """
    CaseAndApi序列化
    """
    data = serializers.SerializerMethodField()

    class Meta:
        model = models.APIandCaseInfo
        fields = '__all__'

    def get_data(self, obj):
        return demjson.encode(obj.data)


##add by yansl@wondershare.cn
##
class EnvSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = models.Env
        fields = "__all__"

    def get_data(self, obj):
        return demjson.encode(obj.data)


class HostSerializer(serializers.ModelSerializer):
    """
    Host序列化
    """

    class Meta:
        model = models.Host
        fields = "__all__"


class DebugTalkSerializer(serializers.ModelSerializer):
    """
    DebugTalk序列化
    """

    class Meta:
        model = models.DebugTalk
        fields = ['id', 'name', 'code']


class SuiteDserializer(serializers.ModelSerializer):
    """
    Suite反序列化
    """

    class Meta:
        model = models.Suite
        fields = ['id', 'name', 'project', 'create_author', 'update_author']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ('id', 'name', 'descr')


class SuiteSerializer(serializers.ModelSerializer):
    """
    Suite序列化
    """
    # suite_project = ProjectSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name')
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    case_info = serializers.SerializerMethodField()

    class Meta:
        model = models.Suite
        fields = (
            'id', 'name', 'project_id', 'project_name', 'create_time', 'update_time', 'create_author', 'update_author',
            'case_info')

    def get_case_info(self, obj):
        case_ids = models.CaseandSuite.objects.filter(suite_id=obj.id).order_by("sort_by")
        case_data = []
        for i in case_ids:
            case = models.CaseInfo.objects.get(id=i.case_id)
            case_data.append({'id': case.id, 'name': case.name})
        return case_data


class Suite2CaseDserializer(serializers.ModelSerializer):
    '''
    套件与用例关联表的序列化
    '''

    class Meta:
        model = models.CaseandSuite
        fields = ['id', 'suite', 'case', 'sort_by']


class TestReportsSerializer(serializers.ModelSerializer):
    """
    TestReports序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    status = serializers.SerializerMethodField()
    is_async = serializers.SerializerMethodField()

    class Meta:
        model = models.TestReports
        fields = ['id', 'name', 'report_name', 'reports_url', 'status', 'testsRun', 'successes', 'failures', 'errors',
                  "is_async",
                  'create_author', 'update_author',
                  "create_time", "update_time"]

    def get_status(self, obj):
        if (obj.status):
            return "成功"
        else:
            return "失败"

    def get_is_async(self, obj):
        if (obj.is_async):
            return "是"
        else:
            return "否"
