#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/26 14:50

from django.utils.deprecation import MiddlewareMixin

class DisableCSRFCheck(MiddlewareMixin):

    def process_request(self, request):
        """
        关闭csrf认证
        :param request:
        """
        setattr(request, '_dont_enforce_csrf_checks', True)
