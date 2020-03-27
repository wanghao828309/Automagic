#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/25 14:29

import django_filters
from webinterface.models import CaseInfo,API,TestReports
from rest_framework import filters


class CaseFilter(filters.FilterSet):
    """
    case模块过滤器
    """

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    project = django_filters.NumberFilter(name="project")
    module = django_filters.NumberFilter(name="module")

    class Meta:
        model = CaseInfo
        fields = ["name","project","module"]

class APIFilter(filters.FilterSet):
    """
    api模块过滤器
    """

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    url = django_filters.CharFilter(name='url', lookup_expr='icontains')
    method = django_filters.CharFilter(name='method')
    project = django_filters.NumberFilter(name="project")
    module = django_filters.NumberFilter(name="module")


    class Meta:
        model = API
        fields = ["name","url","method","project","module"]

class ReportFilter(filters.FilterSet):
    """
    api模块过滤器
    """

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    report_name = django_filters.CharFilter(name='report_name', lookup_expr='icontains')
    is_async = django_filters.CharFilter(name='is_async')


    class Meta:
        model = TestReports
        fields = ["name","report_name","is_async"]