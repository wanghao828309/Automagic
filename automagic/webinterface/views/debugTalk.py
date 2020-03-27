# -*- coding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response
from webinterface.utils import common
from django.http import HttpResponseRedirect
from webinterface.utils import  dbUtil
from django.shortcuts import render_to_response


@api_view(['GET'])
def get_debugtalk(request):
    code = dbUtil.get_debugTalk_datails()
    return render_to_response('debugtalk.html', code)


@api_view(['POST'])
def update_code(request):
    """
    更新DebugTalk信息
    """
    debugtalk = request.POST.get('code')
    code = debugtalk.replace('new_line', '\r\n')
    user = request.user.username
    msg = dbUtil.update_debugTalk_datails(code,user=user)
    res = common.get_msg(msg)
    if res != "OK":
        return Response(res)
    else:
        return HttpResponseRedirect('/api/webinterface/debugtalk')
