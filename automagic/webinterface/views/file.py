#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/1/26 10:05
import os, time,logging
from webinterface import models, serializers
from webinterface.utils import response
from webinterface.utils import common
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import DataError

logger = logging.getLogger('webinterface.views')

class UpFileView(APIView):

    def post(self, request):
        """
        接收文件并保存
        """
        try:
            file = request.FILES['file']
            if not file:
                return Response(response.FILE_IS_NONE)

            file_name = str(int(time.time())) + "_" + file.name
            logger.info("上传到本地文件名称：" + file_name)
            file_path = os.path.join(os.getcwd(), "uploadFile")
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            f = open(os.path.join(file_path, file_name), 'wb')
            for chunk in file.chunks():  # 分块写入文件
                f.write(chunk)

            file_obj = models.FileBinary.objects
            body = {
                "name": file_name,
                "size": common.get_file_size(file.size)
            }
            file_obj.create(**body)
        except DataError:
            return Response(response.DATA_TO_LONG)
        except:
            return Response(response.SYSTEM_ERROR)

        res = {}
        res["fileName"] = file_name
        return Response(res)
