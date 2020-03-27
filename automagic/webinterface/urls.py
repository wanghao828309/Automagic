# -*- coding:utf-8 -*-
"""webinterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from webinterface.views import TestSuiteList
from webinterface.views import case, run, api, env, host, debugTalk, file, report

app_name = 'api'
urlpatterns = [

    # api相关接口
    url(r'^api/(?P<id>\d+)$', api.apiView.as_view({"get": "single"})),
    url(r'^api/list', api.apiView.as_view({"get": "list"})),
    url(r'^api/add$', api.apiView.as_view({"post": "add"})),
    url(r'^api/update$', api.apiView.as_view({"post": "update"})),
    url(r'^api/singledelete$', api.apiView.as_view({"post": "singledelete"})),

    # 用例相关接口
    url(r'^case/(?P<id>\d+)$', case.caseView.as_view({"get": "single"})),
    url(r'^case/list$', case.caseView.as_view({"get": "list"})),
    url(r'^case/add$', case.caseView.as_view({"post": "add"})),
    url(r'^case/update$', case.caseView.as_view({"post": "update"})),
    url(r'^case/delete$', case.caseView.as_view({"post": "delete"})),

    # run相关接口
    url(r'^api/debug', run.debug_api),
    url(r'^api/run', run.run_api),
    url(r'^case/run', run.run_CaseOrSuite),
    url(r'^suite/run', run.run_CaseOrSuite),

    # debugtalk相关接口
    url(r'^debugtalk$', debugTalk.get_debugtalk, name="debugtalklist"),
    url(r'^debugtalk/update$', debugTalk.update_code),

    # 文件上传接口
    url(r'^file', file.UpFileView.as_view()),

    # report接口
    url(r'^report/(?P<id>\d+)$', report.reportView.as_view({"get": "single"})),
    url(r'^report/download/(?P<id>\d+)$', report.reportView.as_view({"get": "download"})),
    url(r'^report/list', report.reportView.as_view({"get": "list"})),

    # add by yansl@wondershare.cn

    # env相关接口
    url(r'^env/(?P<id>\d+)$', env.envView.as_view({"get": "single"})),
    url(r'^env/list$', env.envView.as_view({"get": "list"})),
    url(r'^env/listall$', env.envView.as_view({"get": "list"})),
    url(r'^env/add$', env.envView.as_view({"post": "add"})),
    url(r'^env/update$', env.envView.as_view({"post": "update"})),
    url(r'^env/delete$', env.envView.as_view({"post": "delete"})),

    # Suite相关接口
    url(r'^suite/list$', TestSuiteList.SuiteList.as_view({"get": "list"})),
    url(r'^suite/info$', TestSuiteList.SuiteInfo.as_view()),
    url(r'^suite/add$', TestSuiteList.AddSuite.as_view()),
    url(r'^suite/update$', TestSuiteList.UpdateSuite.as_view()),
    url(r'^suite/delete$', TestSuiteList.DelSuite.as_view()),

    url(r'^host/list$', host.hostView.as_view({"get": "list"})),
    url(r'^host/listAll$', host.hostView.as_view({"get": "listAll"})),
    url(r'^host/add$', host.hostView.as_view({"post": "add"})),
    url(r'^host/update$', host.hostView.as_view({"post": "update"})),
    url(r'^host/delete$', host.hostView.as_view({"post": "delete"})),

]
