# -*- coding:utf-8 -*-
from rest_framework.viewsets import GenericViewSet
from webinterface import models, serializers
from rest_framework.response import Response
from webinterface.utils import response, dbUtil
from webinterface.utils.parser import *
from webinterface.utils.filters import APIFilter
from django.db import DataError, Error
from automated import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication



class apiView(GenericViewSet):
    """
    API操作视图
    """
    serializer_class = serializers.APISerializer
    queryset = models.API.objects
    pagination_class = pagination.MyPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = APIFilter
    # search_fields = ('name','url',)
    ordering_fields = ('id', 'create_time', 'update_time', 'name',)
    ordering = ('-create_time',)
    authentication_classes = (SessionAuthentication,)


    def list(self, request):
        """
        API列表
        """

        try:
            logger.info("当前用户名称：{}".format(self.request.user.username))
            project, apis = "", ""
            product = dbUtil.get_product_byUser(self.request.user.username)
            if product:
                project = dbUtil.get_project_byProduct(product)
                apis = self.get_queryset().filter(project__id__in=project, delStatus=0)
                apis = self.filter_queryset(apis)

            page_apis = self.paginate_queryset(apis)
            serializer = self.get_serializer(page_apis, many=True)

        except KeyError:
            return Response(response.KEY_MISS)
        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        新增一个API
        """

        try:

            testcase_info = request.data
            user = request.user.username
            msg = api_info_logic(user=user, **testcase_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.API_ADD_SUCCESS)

    def update(self, request, **kwargs):
        """
        更新API
        """
        try:
            testcase_info = request.data
            user = request.user.username
            # print("testcase_info:{}".format(testcase_info))
            msg = api_info_logic(user=user, type=False, **testcase_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.API_UPDATE_SUCCESS)


    #add by yansl,去掉批量删除
    def singledelete(self, request, **kwargs):
        """

        删除API
        [{
            index:1
        }]
        """

        try:
            api_info = request.data
            user = request.user.username
            msg = dbUtil.del_single_api_data(user,**api_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.API_DEL_SUCCESS)

    def single(self, request, **kwargs):
        """
        查询单个api，返回body信息
        """
        id = kwargs.pop('id')
        try:
            msg = dbUtil.get_api_datails(id)
            if not isinstance(msg, dict):
                res = common.get_msg(msg)
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except Error:
            return Response(response.SYSTEM_ERROR)
        return Response(msg)
