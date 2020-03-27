# -*- coding:utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import GenericViewSet
from webinterface import models, serializers
from webinterface.utils import response
from webinterface.utils.filters import CaseFilter
from webinterface.utils.parser import *
from django.db import DataError, Error
from rest_framework import filters
from automated import pagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication



class caseView(GenericViewSet):
    """
    case操作视图
    """
    serializer_class = serializers.CaseSerializer
    queryset = models.CaseInfo.objects
    pagination_class = pagination.MyPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = CaseFilter
    #search_fields = ('name',)
    ordering_fields = ('id', 'create_time', 'update_time', 'name',)
    ordering = ('-create_time',)
    authentication_classes = (SessionAuthentication,)

    def list(self, request):
        """
        case列表
        """
        try:
            logger.info("当前用户名称：{}".format(self.request.user.username))
            project, cases = "", ""
            product = dbUtil.get_product_byUser(self.request.user.username)
            if product:
                project = dbUtil.get_project_byProduct(product)
                cases = self.get_queryset().filter(project__id__in=project, delStatus=0)
                cases = self.filter_queryset(cases)
            page_cases = self.paginate_queryset(cases)
            serializer = self.get_serializer(page_cases, many=True)

        except KeyError:
            return Response(response.KEY_MISS)
        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        新增一个case
        """
        try:
            testcase_info = request.data
            user = request.user.username
            msg = case_info_logic(user=user, **testcase_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_ADD_SUCCESS)

    def update(self, request, **kwargs):
        """
        更新case
        """
        try:
            testcase_info = request.data
            user = request.user.username
            msg = case_info_logic(user=user, type=False, **testcase_info)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_UPDATE_SUCCESS)

    def delete(self, request, **kwargs):
        """
        删除case
        [{
            index:1
        }]
        """

        try:
            testcase_info = request.data
            user = request.user.username
            msg = dbUtil.del_case_data(testcase_info,user=user)
            res = common.get_msg(msg)
            if res != "OK":
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_FOUND)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_DEL_SUCCESS)

    def single(self, request, **kwargs):
        """
        查询单个case，返回body信息
        """
        id = kwargs.pop('id')
        try:
            msg = dbUtil.get_case_datails(id)
            if not isinstance(msg, dict):
                res = common.get_msg(msg)
                return Response(res)

        except KeyError:
            return Response(response.KEY_MISS)
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_FOUND)
        except Error:
            return Response(response.SYSTEM_ERROR)

        return Response(msg)

