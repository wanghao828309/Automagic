# -*- coding:utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from webinterface import models, serializers
from rest_framework.response import Response
from webinterface.utils import response, common
from webinterface.utils.parser import *
from django.db import DataError, Error
from automated import pagination
from autoplat.models import Project, Module
from django.db.models import Q


class envView(GenericViewSet):
    """
    env操作视图
    """
    serializer_class = serializers.EnvSerializer
    queryset = models.Env.objects
    pagination_class = pagination.MyPageNumberPagination

    """使用默认分页器"""

    def list(self, request):
        projectid = request.GET.get("projectid")
        envname=request.GET.get("envname")
        if envname== None:
            envname=""
        if envname:
            envs = self.get_queryset().filter(Q(env_name__icontains=envname),delStatus=0).order_by('id')
        else:
            envs = self.get_queryset().filter(delStatus=0).order_by('id')

        page_envs = self.paginate_queryset(envs)
        serializer = self.get_serializer(page_envs, many=True)
        return self.get_paginated_response(serializer.data)

    def listall(self,request):
        serializer = self.get_serializer(self.get_queryset().all(), many=True)
        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        新增一个host配置
        """

        try:
            env_info = request.data
            env_info.create_author=request.user.username;
            env_info.update_author = request.user.username;
            msg = env_info_logic(env_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:

            return Response(response.SYSTEM_ERROR)

        return Response(response.CONFIG_ADD_SUCCESS)

    def update(self, request, **kwargs):
        """
        更新env
        """
        try:
            envs_info={}
            envs_info["env_id"] = request.data.get("env_id")
            envs_info["env_name"] = request.data.get("env_name")
            envs_info["update_author"] = request.user.username
            msg = env_info_logic(envs_info,type=False)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CONFIG_UPDATE_SUCCESS)

    def delete(self, request, **kwargs):
        """
        删除一个接口 pk
        删除多个
        [{
            index:int
        }]
        """

        try:
            envs_info = request.data
            # print testcase_info
            envid = envs_info.get('env_id')
            envs_info.update_author = request.user.username;
            if envid:  # 单个删除
                msg = del_env_data(envid,envs_info.update_author)
                res = common.get_msg(msg)
                if res != "OK":
                    return Response(res)
                msg=del_host_by_envid(envid,envs_info.update_author)
                res = common.get_msg(msg)
                if res != "OK":
                    return Response(res)
            # else:
            #     for content in request.data:
            #         models.API.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)
        return Response(response.CONFIG_UPDATE_SUCCESS)

    def single(self, request, **kwargs):
        """
        查询单个api，返回body信息
        """
        # print kwargs
        env_info = request.data
        envid = env_info.pop('envid')
        try:
            env_info = models.ENV.objects.get(id=envid)
            data = eval(env_info.data)
            # print api_info
        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)
        except Exception:
            return Response(Exception.message)

        # manage_info = {
        #     'request': data,
        #     'name': env_info.name,
        #     'url': env_info.url,
        #     'method': env_info.method,
        # }
        # # print manage_info
        return Response(data)

    def addhost2Env(self,request,**kwargs):
        '''
        添加host
        :param request:
        :param kwargs:
        :return:
        '''
        host_info = request.data
        envid = host_info.pop('envid')
        try:
            env_info = models.ENV.objects.get(id=envid)
            data = eval(env_info.data)
            # print api_info
        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)
        except Exception:
            return Response(Exception.message)
        try:
            msg = host_info_logic(**host_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)
        except Exception:
            return Response(Exception.message)
        return Response(response.CONFIG_ADD_SUCCESS)
