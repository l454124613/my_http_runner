# -*- coding:utf-8 -*-
# Author:lixuecheng

from locust.clients import HttpSession, ResponseContextManager
import json
from base_value.CatchItem import Catch


class MyResponse(ResponseContextManager):

    def __init__(self, response, is_locust=True):
        self.__dict__ = response.__dict__
        # super(MyResponse, self)
        self.is_locust = is_locust

    def failure(self, exc):
        if self.is_locust:
            super(MyResponse, self).failure(exc)
        else:
            print('failure', exc)

    def success(self, exc='运行成功'):
        if self.is_locust:

            super(MyResponse, self).success()
        else:
            print('ok', exc)


class RunHttp:

    def __init__(self, host, is_locust=True, http_session=None, catch_dict=None):
        self.host = host
        if http_session is None:
            self.http_session = HttpSession(host)
        else:
            self.http_session = http_session

        self.is_locust = is_locust
        self.run_dict = {}
        self.order_dict = {}
        self.res_dict = {}
        self.catch_dict = {} if catch_dict is None else catch_dict
        self._add_catch_dict = {}
        self._add_check_dict = {}

    def run(self):

        for i in range(len(self.order_dict)):
            name = self.order_dict[str(i + 1)]
            # try:
            #     self._do_http(self.run_dict[name])
            # except Exception as e:
            #     print('err', e)
            self._do_http(self.run_dict[name])

        class DoRes:
            def __init__(self, res, catch_res):
                self._res = res
                self._catch_res = catch_res

            def get_all_result_dict(self):
                return self._res

            def get_all_result_json(self):
                return json.dumps(self._res)

            def get_catch_dict(self):
                return self._catch_res

            def get_catch_json(self):
                return json.dumps(self._catch_res)

        try:
            return DoRes(self.res_dict, self.catch_dict)
        except Exception as e:
            print('结果解析错误', e)

    def add_request(self, method, path, name=None, params=None, data=None, headers=None, files=None, auth=None,
                    timeout=None, allow_redirects=True, proxies=None, json=None, check=None, catch=None,
                    content_encoding='utf8'):
        info = {}
        if name is None:
            name = path

        # name = path if name is None else name
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        info['name'] = name
        info['data'] = data
        info['files'] = files
        info['headers'] = headers
        info['params'] = params
        # info['method'] = method
        # info['path'] = path
        info['json'] = json
        info['auth'] = auth
        info['timeout'] = timeout
        info['allow_redirects'] = allow_redirects
        info['proxies'] = proxies
        if self.run_dict.get(name) is None:
            self.run_dict[name] = {'method': method, 'url': path, 'info': info, 'check': check, 'catch': catch,
                                   'content_encoding': content_encoding}
            self.order_dict[str(len(self.order_dict) + 1)] = name
        else:
            print('有重复的名字', name)
        return self

    def check_res(self, res, check_dict):

        pass

    '''
    catch_items
    [{name,catch,value}]
    '''

    def add_catch(self, catch_items,res):
        for i in catch_items:
            if type(i) == dict:
                if i.get('name') is not None and i.get('catch') is not None and i.get('catch') in Catch and i.get('value') is not None:
                    pass
            else:
                print('在抓取数据时，格式错误：', i)

        pass

    def add_check(self, check_item):
        pass

    def _do_http(self, key):
        with self.http_session.request(method=key['method'], url=key['url'], catch_response=True, **key['info']) as r:
            r1 = MyResponse(r, self.is_locust)
            if key['check'] is None:
                if r1.ok:
                    r1.success()
                else:
                    r1.failure(r1.reason)
            else:
                if type(key['check']) == list:
                    if len(key['check']) > 0:
                        pass
                    else:
                        if r1.ok:
                            r1.success()
                        else:
                            r1.failure(r1.reason)
                else:
                    r1.failure('校验值输入格式有误')
                    raise Exception('校验值输入格式有误')
            if key['catch'] is None:
                pass
            else:
                pass
            if self.is_locust:
                pass
            else:
                self.res_dict[key['info']['name']] = RunHttp._get_response(r1)

            return RunHttp._get_response(r1, key['content_encoding'])

    def analysis_res(self):
        pass

    @staticmethod
    def _get_response(res, content_encoding='UTF-8'):
        req = {}

        req['method'] = res.request.method
        req['url'] = res.request.url

        # print(type(res.request.headers))
        req['headers'] = {k: j for k, j in res.request.headers.lower_items()}
        result = {}
        result['status_code'] = res.status_code
        try:
            result['json'] = res.json()
        except:
            result['json'] = False
        # try:
        #     result['text'] = res.text
        # except:
        #     result['text'] = 'no'
        try:
            req['auth'] = res.request.auth
        except:
            req['auth'] = False
        try:
            req['files'] = res.request.files
        except:
            req['files'] = False
        try:
            req['data'] = res.request.data
        except:
            req['data'] = False
        # try:
        #     req['params'] = res.request.params
        # except:
        #     req['params'] = 'no'
        # try:
        #     req['params'] = res.request.params
        # except:
        #     req['params'] = 'no'
        result['encoding'] = res.encoding
        result['status_code'] = res.status_code
        result['headers'] = {k: j for k, j in res.headers.items()}
        result['content'] = res.content.decode(content_encoding)
        result['cookies'] = {k: j for k, j in res.cookies.items()}
        result['ok'] = res.ok

        result['request_meta'] = res.locust_request_meta
        result['reason'] = res.reason
        result['request'] = req
        result['elapsed'] = res.elapsed.seconds

        return result


# print(RunHttp('http://172.16.32.40:8082', False).add_request('get',
#                                                              '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd',
#                                                              name='test').run())
# h.add_request('get', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd', name='test')
# # print(**h.run_list[0])
# h.do_http(h.run_dict[h.order_dict['1']])
h = RunHttp('http://www.baidu.com', False).add_request('get', '/', params={'a': 'b'}).run()
print(h.get_all_result_json())
