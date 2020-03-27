# -*- coding:utf-8 -*-
from django.db import models

'''API表操作'''


class APIManager(models.Manager):

    def insert_API(self, **kwargs):
        self.create(project=kwargs.get("project"), module=kwargs.pop("module"),
                    name=kwargs.get("name"),
                    url=kwargs.get("url"),
                    method=kwargs.get("request").get("test").get("request").get("method"),
                    data=kwargs.get("request"),
                    create_author=kwargs.get("author"), update_author=kwargs.get("author"), delStatus=0)

    def update_API(self, **kwargs):
        api = self.get(id=kwargs.pop("index"))
        api.project = kwargs.get("project")
        api.module = kwargs.get("module")
        api.name = kwargs.get("name")
        api.url = kwargs.get("url")
        api.method = kwargs.get("request").get("test").get("request").get("method")
        api.data = kwargs.get("request")
        api.update_author = kwargs.get("author")
        api.save()

    def update_API_data(self, id, data, author):
        api = self.get(id=id)
        api.data = data
        api.update_author = author
        api.save()

    def delete_API(self, id, author):
        api = self.get(id=id)
        api.delStatus = 1
        api.update_author = author
        api.save()

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)


'''case表操作'''


class CaseInfoManager(models.Manager):
    def insert_CaseInfo(self, **kwargs):
        parameters = kwargs.get("parameters")
        if not parameters:
            parameters = "[]"
        self.create(project=kwargs.get("project"), module=kwargs.get("module"),
                    name=kwargs.get("name"),
                    data=parameters,
                    create_author=kwargs.get("author"), update_author=kwargs.get("author"), delStatus=0)

    def update_CaseInfo(self, **kwargs):
        case = self.get(id=kwargs.pop("index"))
        if kwargs.has_key("parameters"):
            case.data = kwargs.get("parameters")
        case.project = kwargs.get("project")
        case.module = kwargs.get("module")
        case.name = kwargs.get("name")
        case.update_author = kwargs.get("author")
        case.save()

    def get_case_name(self, name, module_name, belong_project):
        return self.filter(belong_module__id=module_name).filter(name__exact=name).filter(
            belong_project__exact=belong_project).count()

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)

    def delete_case(self, id, author):
        case = self.get(id=id)
        case.delStatus = 1
        case.update_author = author
        case.save()


'''API与case关联表操作'''


class APIandCaseManager(models.Manager):

    def insert_APIandCase(self, case, api, data, create_author, sortId):
        self.create(caseInfo=case, api=api, data=data, create_author=create_author, update_author=create_author,
                    sort_by=sortId)

    def update_APIandCase_byId(self, id, author, data, sort_by, delStatus=0):
        apiandCase = self.get(id=id)
        apiandCase.update_author = author
        apiandCase.data = data
        apiandCase.sort_by = sort_by
        apiandCase.delStatus = delStatus
        apiandCase.save()

    def delete_APIandCase(self, id, author, delStatus=1):
        apiandCase = self.get(id=id)
        apiandCase.delStatus = delStatus
        apiandCase.update_author = author
        apiandCase.save()

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)


'''DebugTalk表操作'''


class DebugTalkManager(models.Manager):

    def get_by_name(self, name):
        return self.get(name=name, delStatus=0)

    def update_debugTalk(self, name, author, code):
        apiandCase = self.get_by_name(name=name)
        apiandCase.update_author = author
        apiandCase.code = code
        apiandCase.save()


class EnvInfoManager(models.Manager):

    def insert_Env(self, env_name, simple_desc, create_author, update_author):
        self.create(env_name=env_name, simple_desc=simple_desc, create_author=create_author,
                    update_author=update_author, delStatus=0)

    def update_delstatus_byId(self, id, author):
        env = self.get(id=id)
        env.delStatus = 1
        env.update_author = author
        env.save()

    def update_env(self, index, env_name, update_author):
        obj = self.get(id=index)
        obj.env_name = env_name
        obj.update_author = update_author
        obj.save()

    def delete_Env(self, id, author):
        obj = self.get(id=id)
        obj.delStatus = 1
        obj.update_author = author
        obj.save()

    def getAllEnv(self):
        return self.filter(delStatus=0)

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)

    def get_by_name(self, name):
        return self.get(env_name=name, delStatus=0)


class HostManager(models.Manager):

    def insert_Host(self, hostinfo):
        env_id = hostinfo.get("env_id")
        base_url = hostinfo.get("base_url")
        host = hostinfo.get("host")
        simple_desc = hostinfo.get("simple_desc")
        if (simple_desc == None):
            simple_desc = " "
        create_author = hostinfo.get("create_author")
        update_author = hostinfo.get("update_author")
        hostInfo = self.create(env_id=env_id, base_url=base_url, host=host, simple_desc=simple_desc,
                               update_author=update_author, create_author=create_author)
        return hostInfo

    def update_delstatus_byId(self, id, author):
        Host = self.get(id=id)
        Host.delStatus = 1
        Host.update_author = author
        Host.save()

    def update_Host(self, hostinfo):
        base_url = hostinfo.get("base_url")
        host = hostinfo.get("host")
        simple_desc = hostinfo.get("simple_desc")
        update_author = hostinfo.get("update_author")
        hostid = hostinfo.get("hostid")

        Host = self.get(id=hostid)
        Host.update_author = update_author
        Host.base_url = base_url
        Host.host = host
        Host.simple_desc = simple_desc
        Host.save()

    def del_Host(self, id, update_author):

        host = self.get(id=id)
        host.delStatus = 1
        host.update_author = update_author
        host.save()

    def delete_by_env(self, env_id, author):
        obj = self.filter(env_id=env_id)
        for i in obj:
            i.delStatus = 1
            i.update_author = author
            i.save()

    def get_by_env_id(self, env_id):
        return self.filter(env_id=env_id, delStatus=0)


'''suite表操作'''


class SuiteManager(models.Manager):

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)


'''Reports表操作'''


class TestReportsManager(models.Manager):
    def insert_Reports_noAsync(self, **kwargs):
        self.create(report_name=kwargs.get("report_name"), reports_url=kwargs.get("reports_url"),
                    status=kwargs.get("status"), testsRun=kwargs.get("testsRun"), successes=kwargs.get("successes"),
                    failures=kwargs.get("failures"), errors=kwargs.get("errors"),
                    create_author=kwargs.get("create_author"), name=kwargs.get("name"), is_async=0)

    def insert_Reports_Async(self, **kwargs):
        self.create(report_name=kwargs.get("report_name"), reports_url=kwargs.get("reports_url"),
                    status=kwargs.get("status"), testsRun=kwargs.get("testsRun"), successes=kwargs.get("successes"),
                    failures=kwargs.get("failures"), errors=kwargs.get("errors"),
                    create_author=kwargs.get("create_author"), is_async=1)

    def get_by_id(self, id):
        return self.get(id=id, delStatus=0)


if __name__ == "__main__":
    EnvInfoManager().insert_Env(1, 'stg', 'stg', 'yansl', 'yansl')
