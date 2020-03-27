# -*- coding:utf-8 -*-
from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class MyCursorPagination(pagination.CursorPagination):

    # def __init__(self,page_size):
    #     super.__init__();
    #     self.page_size=page_size

    """
    Cursor 光标分页 性能高，安全
    """
    # 每页的默认显示数量
    page_size = 1
    # 排序方式
    ordering = '-update_time'
    page_size_query_param = "pages"
    max_page_size = 20


class MyPageNumberPagination(pagination.PageNumberPagination):
    """
    普通分页，数据量越大性能越差
    """
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 100

    """
     自定义分页方法
    """
    def get_paginated_response(self, data):
        """
        设置返回内容格式
        """

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            # ('page', self.get_html_context()),
            ('results', data)
        ]))



