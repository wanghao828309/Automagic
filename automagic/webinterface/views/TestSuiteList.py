# encoding= utf-8
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import DjangoFilterBackend, SearchFilter, OrderingFilter
from rest_framework import filters
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from webinterface.utils.api_response import JsonResponse, Response
from webinterface.models import Suite, CaseInfo, Project, CaseandSuite
from webinterface.serializers import SuiteSerializer, SuiteDserializer, Suite2CaseDserializer
from rest_framework.viewsets import GenericViewSet
from webinterface.utils import response, dbUtil

import django_filters
from automated import pagination

logger = logging.getLogger(__name__)


class SuiteFilter(filters.FilterSet):
    # id必须为数字类型
    project_id = django_filters.NumberFilter(name="project_id")
    # 名称中包含某字符，且字符不区分大小写
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = Suite
        fields = ['project_id', 'name']


# 查看单个suite详情
class SuiteInfo(APIView):
    def get(self, request):
        """
        获取项目详情
        :param request:
        :return:
        """
        suite_id = request.GET.get("id")
        if not suite_id:
            return JsonResponse(code="999996", msg="参数有误！")
        # 查找suite是否存在
        try:
            obj = Suite.objects.get(id=suite_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="Suite不存在！")
        serialize = SuiteSerializer(obj)
        from webinterface.utils import dbUtil
        product = dbUtil.get_product_byProject(obj.project.name)
        res = serialize.data
        res["product"] = product.productid.name
        return Response(res)


# 添加测试套件
class AddSuite(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 project_id, module_id, name，suite_case
            if not data["suite_name"] or not data["project_id"] or not data["case_ids"]:
                return JsonResponse(code="10002", msg="必填参数内容为空！")
        except KeyError:
            return JsonResponse(code="10003", msg="4！")
        try:
            Project.objects.get(id=data['project_id'])
        except:
            return JsonResponse(code="10004", msg="项目不存在！")

    # 添加suite对应的case
    def add_suite_case(self, suite_id, case_id, sort):
        suitecase_serializer = Suite2CaseDserializer(data={
            "suite": suite_id,
            "case": case_id,
            "sort_by": sort
        })
        try:
            suite_info = Suite.objects.get(id=suite_id)
            case_info = CaseInfo.objects.get(id=case_id)
            if suitecase_serializer.is_valid():
                suitecase_serializer.save(suite=suite_info, case=case_info)
        except:
            return JsonResponse(code="10004", msg="case不存在！")

    # 对外提供post接口
    def post(self, request):
        """
        新增 Test Suite api
        :param request:
        :return: json
        """
        data = JSONParser().parse(request)
        if request.user.username == '':
            return JsonResponse(code="10005", msg="当前用户不存在！")

        result = self.parameter_check(data)
        if result:
            return result
        serializer = SuiteDserializer(data={
            "name": data["suite_name"],
            "project": data["project_id"],
            "create_author": request.user.username,
            "update_author": request.user.username
        })
        project = Project.objects.get(id=data['project_id'])
        with transaction.atomic():
            print serializer.is_valid()
            if serializer.is_valid():
                # 保存suite
                serializer.save(project=project)
                # 保存suite对应的case
                for case_id in data["case_ids"]:
                    self.add_suite_case(serializer.data.get("id"), case_id, data["case_ids"].index(case_id))
                return JsonResponse(data={
                    "suite_id": serializer.data.get("id")
                }, code="10000", msg="新增suite成功")
            else:
                return JsonResponse(code="10001", msg="序列化suite失败")


# 删除测试套件
class DelSuite(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验suite_id类型为int
            print data["ids"]
            if not isinstance(data["ids"], list):
                return JsonResponse(code="20002", msg="参数不是list类型！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="20003", msg="id必须为int类型！")
        except KeyError:
            return JsonResponse(code="20004", msg="参数key有误！")

    def post(self, request):
        """
        删除Test Suite api，支持批量删除
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result

        for i in data["ids"]:
            try:
                Suite.objects.get(id=i)
            #     if not request.user.is_superuser:
            #         return JsonResponse(code="999983", msg=str(obj)+"无操作权限！")
            except ObjectDoesNotExist:
                return JsonResponse(code="20001", msg="id=%s不存在" % i)
        with transaction.atomic():
            for j in data["ids"]:
                Suite.objects.filter(id=j).delete()
                CaseandSuite.objects.filter(id=j).delete()
            return JsonResponse(code="20000", msg="删除成功")


# 更新测试套件
class UpdateSuite(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 suite_id, case_ids, name
            if not data["suite_name"] or not data["case_ids"] or not data["id"] or not data["project_id"]:
                return JsonResponse(code="30001", msg="参数内容为空！")
        except KeyError:
            return JsonResponse(code="30002", msg="缺少必填参数！")
        # suite是否存在
        try:
            Suite.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="30003", msg="suite不存在!")
        # project是否存在
        try:
            Project.objects.get(id=data['project_id'])
        except ObjectDoesNotExist:
            return JsonResponse(code="30004", msg="project不存在!")

    def update_suite_case(self, data):
        old_list = list(CaseandSuite.objects.filter(suite_id=data["id"]))
        for i in data["case_ids"]:
            obj = CaseandSuite.objects.filter(suite_id=data["id"], case_id=i).first()
            if obj in old_list:
                # 如果存在则更新
                suitecase_serializer = Suite2CaseDserializer(obj, data={
                    "suite": data["id"],
                    "case": i,
                    "sort_by": data["case_ids"].index(i)
                })
                # suite_info = Suite.objects.get(id=suite_id)
                # case_info = CaseInfo.objects.get(id=case_id)
                if suitecase_serializer.is_valid():
                    suitecase_serializer.save()
                old_list.remove(obj)

            else:
                # 新增无法匹配的
                suitecase_serializer = Suite2CaseDserializer(data={
                    "suite": data["id"],
                    "case": i,
                    "sort_by": data["case_ids"].index(i)
                })
                # suite_info = Suite.objects.get(id=suite_id)
                # case_info = CaseInfo.objects.get(id=case_id)
                if suitecase_serializer.is_valid():
                    suitecase_serializer.save()
        # 删除多余的
        for j in old_list:
            j.delete()

        # suitecase_serializer = Suite2CaseDserializer(data={
        #     "suite": suite_id,
        #     "case": case_id
        # })
        # case_suite = CaseandSuite.objects.get(case_id=suite_id)
        #
        # if suitecase_serializer.is_valid():
        #     for i in case_suite:
        #         suitecase_serializer.update(instance=case_suite, validated_data =  )

    # 对外提供POST接口
    def post(self, request):
        """
        新增 Test Suite api
        :param request:
        :return: json
        """
        data = JSONParser().parse(request)
        if request.user.username == '':
            return JsonResponse(code="30005", msg="当前用户不存在！")
        result = self.parameter_check(data)
        if result:
            return result
        obj = Suite.objects.get(id=data["id"])
        serializer_data = {"id": data["id"],
                           "name": data["suite_name"],
                           "project": data["project_id"],
                           "create_author": obj.create_author,
                           "update_author": request.user.username
                           }
        obj = Suite.objects.get(id=data["id"])
        suite_ser = SuiteDserializer(obj, data=serializer_data)
        with transaction.atomic():
            if suite_ser.is_valid():
                # 更新suite表
                suite_ser.save()
                # 更新suiteandCase表
                self.update_suite_case(data)
                return JsonResponse(data={"id": suite_ser.data.get("id")}, code="30000", msg="更新成功")
            else:
                return JsonResponse(data={}, code="30006", msg="参数格式不正确")


# 测试套件列表
class SuiteList(GenericViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    queryset = Suite.objects
    pagination_class = pagination.MyPageNumberPagination
    # 使用过滤器
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 指定搜索字段
    filter_class = SuiteFilter
    # search_fields = {'name',}
    ordering_fields = ('id', 'create_time', 'update_time', 'name',)
    ordering = ('-create_time',)
    serializer_class = SuiteSerializer

    def list(self, request):
        """
        API列表
        """

        try:
            logger.info("当前用户名称：{}".format(self.request.user.username))
            project, suites = "", ""
            product = dbUtil.get_product_byUser(self.request.user.username)
            if product:
                project = dbUtil.get_project_byProduct(product)
                suites = self.get_queryset().filter(project__id__in=project, delStatus=0)
                suites = self.filter_queryset(suites)

            page_suites = self.paginate_queryset(suites)
            serializer = self.get_serializer(page_suites, many=True)

        except KeyError:
            return Response(response.KEY_MISS)
        return self.get_paginated_response(serializer.data)


