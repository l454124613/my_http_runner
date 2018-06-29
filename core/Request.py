# -*- coding:utf-8 -*-
# Author:lixuecheng
from requests import sessions
# from locust.clients import HttpSession
import time
import sys
from base_value.ResponseItem import ResponseItem
import re


# global ff
ff = []

is_ok = True


class Request:
    ff = []

    def __init__(self, http_session=None, not_locust=True, catch_dict=None):
        self.HttpSession = http_session
        self._not_locust = not_locust
        self.run_item_list = []
        self.res_dict = {}
        self.catch_dict = {} if catch_dict is None else catch_dict
        self._add_catch_dict = {}
        self._add_check_dict = {}
        pass

    def on_start(self):
        pass

    def on_end(self):
        pass

    def set_locust_host(self, host):
        if not host.startswith('http'):
            host = 'http://' + host
        from locust.clients import HttpSession
        self.HttpSession = HttpSession(host)
        print('set session ok:' + host)
        return self

    def is_locust(self):
        self._not_locust = False
        return self

    def run(self):
        # time.sleep(1)
        print('run ok')
        self.run_item_list = []
        pass

    def add_check(self, check):
        pass

    def add_catch(self, catch):
        pass

    def add_request(self, method, url, name=None, params=None, data=None, headers=None, files=None, auth=None,
                    timeout=None, allow_redirects=True, proxies=None, json=None, check=None, catch=None,
                    content_encoding='utf8'):
        print('add req ok')
        if name is None:
            name = url

        # name = path if name is None else name
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        self.run_item_list.append(
            dict(method=method, url=url, name=name, params=params, data=data, headers=headers, files=files, auth=auth,
                 timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, json=json, check=check, catch=catch,
                 content_encoding=content_encoding))

        return self

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
                    # print(a1)

                    if a1 is not None:
                        s = s.replace('${%s}' % i, a1)
                return s
            else:
                return s

    def _generator_key(self):
        for i in self.run_item_list:
            info = dict()
            info['name'] = self._reg_get_all(i.get('name'))
            info['data'] = self._reg_get_all(i.get('data'))
            info['files'] = i.get('files')
            info['headers'] = self._reg_get_all(i.get('headers'))
            info['params'] = self._reg_get_all(i.get('params'))
            # info['method'] = method
            # info['path'] = path
            info['json'] = self._reg_get_all(i.get('json'))
            info['auth'] = i.get('auth')
            info['timeout'] = i.get('timeout')
            info['allow_redirects'] = i.get('allow_redirects')
            info['proxies'] = i.get('proxies')
            yield {'method': i.get('method'), 'url': self._reg_get_all(i.get('path')), 'info': info,
                   'check': i.get('check'),
                   'catch': i.get('catch'),
                   'content_encoding': i.get('content_encoding')}

    @staticmethod
    def _catch_check_res(item, res, content_encoding):
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
                            if str(i.get('value')) =='None':
                                check_result += ('\n获取%s,结果为：%s,期望为：%s,实际是：%s' % (
                                    i.get('response_item').name, r3, str(i.get('value')), str(r2)))

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
    @staticmethod
    def _get_response(res, content_encoding='UTF-8'):
        req11 = dict()

        req11['method'] = res.request.method
        req11['url'] = res.request.url

        # print(type(res.request.headers))
        req11['headers'] = {k: j for k, j in res.request.headers.lower_items()}
        result = dict()
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
            req11['auth'] = res.request.auth
        except:
            req11['auth'] = False
        try:
            req11['files'] = res.request.files
        except:
            req11['files'] = False
        try:
            req11['data'] = res.request.data
        except:
            req11['data'] = False
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

        try:
            result['content'] = res.content.decode(content_encoding)
        except UnicodeDecodeError:
            try:
                result['content'] = res.content.decode('gbk')
            except:
                result['content'] = res.content.decode('utf-8', "ignore")
        result['cookies'] = {k: j for k, j in res.cookies.items()}
        result['ok'] = res.ok

        result['request_meta'] = res.locust_request_meta
        result['reason'] = res.reason
        result['request'] = req11
        result['elapsed'] = res.elapsed.seconds

        return result


def run(fn):
    def aa(*c):
        return fn(*c)

    ff.append(fn.__name__)
    print(1)
    return aa


def _check_ok():
    if 'wei_le_pi_liang_yun_xing' in sys.path:
        return False
    else:
        return True


def runnable(cls):
    if _check_ok():
        c = cls()
        c.on_start()
        for i in ff:
            if hasattr(c, i):
                c1 = getattr(c, i)
                c1()
        c.on_end()
    else:
        Request.ff = ff
    return cls
