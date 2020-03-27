# -*- coding:utf-8 -*-
from rest_framework.viewsets import GenericViewSet
from webinterface import models, serializers
from rest_framework.response import Response
from webinterface.utils import response
from webinterface.utils.parser import *
from webinterface.utils.filters import ReportFilter
from automated import pagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from django.http import StreamingHttpResponse
import os


class reportView(GenericViewSet):
    """
    Report操作视图
    """
    serializer_class = serializers.TestReportsSerializer
    queryset = models.TestReports.objects
    pagination_class = pagination.MyPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_class = ReportFilter
    # search_fields = ('name','url',)
    ordering_fields = ('id', 'create_time', 'update_time', 'name',)
    ordering = ('-create_time',)
    authentication_classes = (SessionAuthentication,)

    def list(self, request):
        """
        Report列表
        """

        try:
            logger.info("当前用户名称：{}".format(self.request.user.username))
            reports = self.get_queryset().all()
            reports = self.filter_queryset(reports)
            page_Reports = self.paginate_queryset(reports)
            serializer = self.get_serializer(page_Reports, many=True)

        except KeyError:
            return Response(response.KEY_MISS)
        return self.get_paginated_response(serializer.data)

    def single(self, request, **kwargs):
        """
        查询单个Report，返回reports_url
        """
        id = kwargs.pop('id')
        try:
            report_obj = self.get_queryset().get(id=id)
            res = {}
            res["url"] = report_obj.reports_url
        except KeyError:
            return Response(response.KEY_MISS)
        except:
            return Response(response.SYSTEM_ERROR)
        return Response(res)

    def download(self, request, **kwargs):
        """
        下载报告文件
        :param request:
        :param kwargs:
        :return:
        """
        id = kwargs.pop('id')
        summary = self.get_queryset().get(id=id)
        report_name = summary.report_name
        report_path = os.path.join(os.getcwd(), "reports", report_name, report_name + ".html")
        logger.info("下载的报告路径是：{}".format(report_path))
        if not os.path.exists(report_path):
            from webinterface.utils import response
            return Response(response.FILE_NOT_EXISTS)

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(report_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(report_name + '.html')
        return response
