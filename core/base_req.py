# -*- coding:utf-8 -*-
# Author:lixuecheng

from locust.clients import HttpSession, ResponseContextManager
import json
from base_value.ResponseItem import ResponseItem
import re


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

    def _reg_get_all(self, s):
        if type(s) is dict:
            return self._reg_get_dict(s)
        elif type(s) is list:
            return self._reg_get_list(s)
        else:
            return self._reg_get(s)

    def _reg_get_list(self, s):
        if len(s) > 0:
            for i in len(s):
                s[i] = self._reg_get_all(s[i])
            return s
        else:
            return s

    def _reg_get_dict(self, s):

        if type(s) is dict:
            if len(s) > 0:
                for j, k in s.items():
                    s[j] = self._reg_get_all(k)
                return s
            else:
                return s

    def _reg_get(self, s):
        if s is None or s == [] or s == {}:
            return s
        else:
            p = re.compile(r'\$\{(.*?)\}')
            s1 = p.findall(s)
            if len(s1) > 0:
                for i in s1:
                    a1 = self.catch_dict.get(i)
                    if a1 is not None:
                        s.replace('${%s}' % i, a1)
                return s
            else:
                return s

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
        info['name'] = self._reg_get_all(name)
        info['data'] = self._reg_get_all(data)
        info['files'] = files
        info['headers'] = self._reg_get_all(headers)
        info['params'] = self._reg_get_all(params)
        # info['method'] = method
        # info['path'] = path
        info['json'] = self._reg_get_all(json)
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

    def add_catch(self, catch_items):
        pass

    def add_check(self, check_item):
        pass

    def _catch_check_res(self, item, res, content_encoding):
        try:

            if item.get('response_item') is not None and item.get('response_item') in ResponseItem:

                if item.get('way') is not None:
                    if item.get('response_item') is ResponseItem.content:

                        p = re.compile(item.get('way'))
                        p2 = p.findall(res.content.decode(content_encoding))
                        if len(p2) == 1:
                            return p2[0]
                        elif len(p2) < 1:
                            return None
                        else:
                            print("正则匹配到多个结果，默认选择第一个:", item.get('way'))
                            return p2[0]
                    elif item.get('response_item') is ResponseItem.json:
                        json = res.json()
                        return eval(item.get('way'))
                    elif item.get('response_item') is ResponseItem.cookies:
                        cookie = {k: j for k, j in res.cookies.items()}
                        return eval(item.get('way'))

                    elif item.get('response_item') is ResponseItem.headers:
                        header = {k: j for k, j in res.headers.items()}
                        return eval(item.get('way'))
                    elif item.get('response_item') is ResponseItem.encoding:

                        return res.encoding
                    elif item.get('response_item') is ResponseItem.status_code:
                        return res.status_code

                    else:
                        print('在提取数据时，发生错误：', item)
                        return None

                else:
                    if item.get('response_item') is ResponseItem.encoding:
                        return res.encoding
                    elif item.get('response_item') is ResponseItem.status_code:
                        return res.status_code
                    else:
                        print('在提取数据时，发生错误：', item)
                        return None

            else:
                print('在抓取数据时，抓取项格式错误：', item)
                return None
        except Exception as e:
            print('在解析数据时，发生错误：', e)
            return None

    def catch_res(self, catch_items, res, is_dict, content_encoding):

        if is_dict:

            if catch_items.get('name') is not None:
                catch_result = self._catch_check_res(catch_items, res, content_encoding)
                if catch_result is not None:
                    self.catch_dict[catch_items['name']] = catch_result

        else:
            for i in catch_items:
                if type(i) == dict:
                    if i.get('name') is not None:
                        catch_result = self._catch_check_res(i, res, content_encoding)
                    if catch_result is not None:
                        self.catch_dict[i['name']] = catch_result
                else:
                    print('在抓取数据时，格式错误：', i)

    def check_res(self, check_items, res, is_dict, content_encoding):

        if is_dict:
            if check_items['value'] is not None:
                check_result = self._catch_check_res(check_items, res, content_encoding)
                if check_result is None:
                    return False, '没有找到匹配的值匹配：' + str(check_items.get('value'))
                else:
                    r3 = (str(check_result) == str(check_items.get('value')))
                    return r3, '获取' + check_items.get('response_item').name + ',结果为：' + str(r3) + ',实际获取：' + str(
                        check_result) + ',期望等于：' + str(
                        check_items.get('value'))
            else:
                print('输入格式有误，请检查：', check_items)
                return False, "输入格式有误，请检查：" + check_items

        else:
            is_ok = True
            check_result = ''
            for i in check_items:
                if type(i) == dict:
                    if i.get('value') is not None:
                        r2 = self._catch_check_res(i, res, content_encoding)
                        if r2 is None:
                            # return False, '输入格式有误，请检查：'+i
                            is_ok = False
                            check_result = check_result + '\n没有找到匹配的值匹配：' + i
                            # [{'result': False, 'value': str(check_items.get('value')), 'actual': str(r2)}]
                        else:
                            r3 = (str(r2) == str(i.get('value')))
                            is_ok = (is_ok and r3)
                            check_result += ('\n获取%s,结果为：%s,期望为：%s,实际是：%s' % (
                                i.get('response_item').name, r3, str(i.get('value')), str(r2)))

                    else:
                        print('输入格式有误，请检查：', i)
                        check_result = check_result + '\n输入格式有误，请检查' + i
            return is_ok, check_result

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
                        r2 = self.check_res(key['check'], r1, False, key['content_encoding'])
                        if r2[0]:
                            r1.success()
                        else:
                            r1.failure(r2[1])

                    else:
                        if r1.ok:
                            r1.success()
                        else:
                            r1.failure(r1.reason)
                else:
                    if type(key['check']) == dict:
                        r2 = self.check_res(key['check'], r1, True, key['content_encoding'])
                        if r2[0]:
                            r1.success()
                        else:
                            r1.failure(r2[1])

                    else:
                        r1.failure('校验值输入格式有误')
                        raise Exception('校验值输入格式有误')
            if key['catch'] is None:
                pass
            else:
                if type(key['catch']) == list and len(key['catch']) > 0:
                    self.catch_res(key['catch'], r1, False, key['content_encoding'])
                elif type(key['catch']) == dict:
                    self.catch_res(key['catch'], r1, True, key['content_encoding'])
                else:
                    print("抓取数据格式不正确", key['catch'])

            if self.is_locust:
                pass
            else:
                self.res_dict[key['info']['name']] = RunHttp._get_response(r1)

            return RunHttp._get_response(r1, key['content_encoding'])

    def analysis_res(self):
        pass

    @staticmethod
    def _get_response(res, content_encoding='UTF-8'):
        req11 = {}

        req11['method'] = res.request.method
        req11['url'] = res.request.url

        # print(type(res.request.headers))
        req11['headers'] = {k: j for k, j in res.request.headers.lower_items()}
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
        result['request'] = req11
        result['elapsed'] = res.elapsed.seconds

        return result


catch = [{'name': 'test1', 'response_item': ResponseItem.json, 'way': "json['resultData']['access_token1']"}
    , {'name': 'test2', 'response_item': ResponseItem.content, 'way': r'"access_token":"(.*?)"'}
    , {'name': 'cookie', 'response_item': ResponseItem.cookies, 'way': '111'}
    , {'name': 'header', 'response_item': ResponseItem.headers, 'way': 'header["Content-Type"]'}
    , {'name': 'encoding', 'response_item': ResponseItem.encoding, 'way': 'header1["Content-Type"]'}
    , {'name': 'status_code', 'response_item': ResponseItem.status_code, 'way': 'header["Content-Type"]'}]
check = {'response_item': ResponseItem.status_code, 'value': '201'}
# , {'response_item': ResponseItem.json, 'value': '0', 'way': "json['errNo']"}]
a = RunHttp('http://172.16.32.40:8082', False).add_request('get',
                                                           '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd',
                                                           name='test', check=check).run()
# print(a.get_all_result_dict())
# print(a.get_catch_dict())
# h.add_request('get', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd', name='test')
# # print(**h.run_list[0])
# h.do_http(h.run_dict[h.order_dict['1']])
# h = RunHttp('http://www.baidu.com', False).add_request('get', '/', params={'a': 'b'}).run()
# print(h.get_all_result_json())
