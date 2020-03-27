# -*- coding:utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from webinterface import models, serializers
from rest_framework.response import Response
from webinterface.utils import response, common
from webinterface.utils.parser import *
from django.db import DataError, Error
from automated import pagination
from django.db.models import Q
from django.http import HttpResponse
import demjson
import json
from django.http import JsonResponse


class hostView(GenericViewSet):
    """
    env操作视图
    """
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects
    pagination_class = pagination.MyPageNumberPagination
    """使用默认分页器"""

    def list(self, request):
        env_id=request.GET.get("env_id")
        base_url = request.GET.get("base_url")
        host = request.GET.get("host")
        if base_url == None:
            base_url=""
        if host == None:
            host=""
        if base_url or host:
            host = self.get_queryset().filter(Q(base_url__icontains=base_url) | Q(host__icontains=host),env_id=env_id, delStatus=0).order_by('id')
        else:
            host = self.get_queryset().filter(env_id=env_id,delStatus=0).order_by('id')
        page_host = self.paginate_queryset(host)
        serializer = self.get_serializer(page_host, many=True)
        return self.get_paginated_response(serializer.data)


    #获取环境列表
    def listAll(self, request):
        ret=[]
        EnvQuery = models.Env.objects
        HostQuery = models.Host.objects
        envs=EnvQuery.getAllEnv()
        for env in envs:
            tmpHost = {}
            tmpHost["env_name"]=env.env_name
            tmpHost["env_id"]=env.id;
            hosts = HostQuery.get_by_env_id(env.id)
            hostList=[]
            for h in hosts:
                tmpHostDetail = {}
                tmpHostDetail["host_id"] = h.id
                tmpHostDetail["url"]=h.base_url
                tmpHostDetail["host"]=h.host
                hostList.append(tmpHostDetail)
            tmpHost["env_detail"]=hostList
            ret.append(tmpHost)
        json=demjson.encode(ret,"utf-8")
        return HttpResponse(json)


    def add(self, request):
        """
        新增一个host配置
        """

        try:
            host_info = request.data
            host_detail={}
            host_detail["env_id"]=host_info.get("env_id")
            host_detail["base_url"] = host_info.get("base_url")
            host_detail["host"] = host_info.get("host")
            # print("testcase_info:{}".format(testcase_info))
            host_detail["create_author"]=request.user.username
            host_detail["update_author"] = request.user.username
            host_info = host_info_logic(host_detail)
            res={}
            res["id"]=host_info.id
            res["success"]="success"
            return JsonResponse(res, safe=False)

        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CONFIG_ADD_SUCCESS)

    def update(self, request):
        """
        更新host
        """
        try:
            host_info = request.data
            host_detail = {}
            host_detail["hostid"] = host_info.get("hostid")
            host_detail["base_url"] = host_info.get("base_url")
            host_detail["host"] = host_info.get("host")
            host_detail["simple_desc"] = " "
            # print("testcase_info:{}".format(testcase_info))
            host_detail["create_author"] = request.user.username
            host_detail["update_author"] = request.user.username
            # print("testcase_info:{}".format(testcase_info))
            msg = host_info_logic(host_detail,type=False)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CONFIG_UPDATE_SUCCESS)

    def delete(self, request):
        """
        """

        try:

            host_info = request.data

            msg = del_host_data(host_info.get("id"),request.user.username)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)
        return Response(response.CONFIG_UPDATE_SUCCESS)
