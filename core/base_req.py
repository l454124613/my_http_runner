# -*- coding:utf-8 -*-
# Author:lixuecheng

from locust.clients import HttpSession, ResponseContextManager


class MyResponse(ResponseContextManager):
    encoding = 'UTF-8'

    def __init__(self, response, is_locust=True):
        self.__dict__ = response.__dict__
        # super(MyResponse, self)
        self.is_locust = is_locust

    def failure(self, exc):
        if self.is_locust:
            super(MyResponse, self).failure(exc)
        else:
            print(exc)

    def success(self, exc):
        if self.is_locust:

            super(MyResponse, self).success()
        else:
            print(exc)


host = 'http://172.16.32.40:8082'
v = HttpSession(host)
"""Constructs a :class:`Request <Request>`, prepares it and sends it.
   Returns :class:`Response <Response>` object.

   :param method: method for the new :class:`Request` object.
   :param url: URL for the new :class:`Request` object.
   :param params: (optional) Dictionary or bytes to be sent in the query
       string for the :class:`Request`.
   :param data: (optional) Dictionary, bytes, or file-like object to send
       in the body of the :class:`Request`.
   :param json: (optional) json to send in the body of the
       :class:`Request`.
   :param headers: (optional) Dictionary of HTTP Headers to send with the
       :class:`Request`.
   :param cookies: (optional) Dict or CookieJar object to send with the
       :class:`Request`.
   :param files: (optional) Dictionary of ``'filename': file-like-objects``
       for multipart encoding upload.
   :param auth: (optional) Auth tuple or callable to enable
       Basic/Digest/Custom HTTP Auth.
   :param timeout: (optional) How long to wait for the server to send
       data before giving up, as a float, or a :ref:`(connect timeout,
       read timeout) <timeouts>` tuple.
   :type timeout: float or tuple
   :param allow_redirects: (optional) Set to True by default.
   :type allow_redirects: bool
   :param proxies: (optional) Dictionary mapping protocol or protocol and
       hostname to the URL of the proxy.
   :param stream: (optional) whether to immediately download the response
       content. Defaults to ``False``.
   :param verify: (optional) Either a boolean, in which case it controls whether we verify
       the server's TLS certificate, or a string, in which case it must be a path
       to a CA bundle to use. Defaults to ``True``.
   :param cert: (optional) if String, path to ssl client cert file (.pem).
       If Tuple, ('cert', 'key') pair.
   :rtype: requests.Response
"""


def run_http(h, is_locust=True):
    header = {"Cookie": 'asdasda=123123'}
    with h.request('get', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd',
                   catch_response=True, name='getToken') as r:
        r1 = MyResponse(r, is_locust)
        # print(r1.json())
        print(r1.status_code)
        # print([k+"="+v for k,v in r1.headers.items()])
        # try:
        #     print(r1.request.method)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.url)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.headers)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.files)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.data)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.json)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.params)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.auth)
        # except Exception as e:
        #     print(e)
        # try:
        #     print([i for i in r1.request._cookies])
        # except Exception as e:
        #     print(e)

        # print(r1.request)

        print(r1.json())

        # print(r1.content)
        # print([r1.cookies.items()])
        # print(r1.ok)
        # print(r1.encoding)
        # r1.failure('err')
        # r1.success('ok')

        # print(r1.locust_request_meta)
        # print(r1.raise_for_status())
        # print(r1.text)

        # print(r1.reason)
        # print(r1.elapsed)


# run_http(v, False)


class RunHttp:
    def __init__(self, host, is_locust=True):
        self.host = host
        self.http_session = HttpSession(host)
        self.is_locust = is_locust
        self.run_dict = {}
        self.order_dict = {}
        self.res_dict = {}

    def run(self):
        for i in range(len(self.order_dict)):
            name = self.order_dict[str(i + 1)]
            try:
                res = self._do_http(self.run_dict[name])
                self.res_dict[name] = res
                return res
            except Exception as e:
                print('err', e)

    def add_request(self, method, path, name=None, params=None, data=None, headers=None, files=None, auth=None,
                    timeout=None, allow_redirects=True, proxies=None, json=None, check=None):
        info = {}
        if name is None:
            name = path

        # name = path if name is None else name
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        # info['name'] = name
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
            self.run_dict[name] = {'method': method, 'url': path, 'info': info, 'check': check}
            self.order_dict[str(len(self.order_dict) + 1)] = name
        else:
            print('有重复的名字', name)
        return self

    def _do_http(self, key):

        with self.http_session.request(method=key['method'], url=key['url'], catch_response=True, **key['info']) as r:
            r1 = MyResponse(r, self.is_locust)
            return self._get_response(r1)

    def analysis_res(self):
        pass

    def _get_response(self, res):
        result = {}
        req = {'method': res.request.method, 'url': res.request.url, 'headers': res.request.headers}
        result['status_code'] = res.status_code
        try:
            result['json'] = res.json()
        except:
            result['json'] = None
        try:
            result['text'] = res.text
        except:
            result['text'] = None
        try:
            req['auth'] = res.request.auth
        except:
            req['auth'] = None
        try:
            req['files'] = res.request.files
        except:
            req['files'] = None
        try:
            req['data'] = res.request.data
        except:
            req['data'] = None
        try:
            req['json'] = res.request.json
        except:
            req['json'] = None
        try:
            req['params'] = res.request.params
        except:
            req['params'] = None

        result['status_code'] = res.status_code
        result['headers'] = [k + "=" + j for k, j in res.headers.items()]
        result['content'] = res.content
        result['cookies'] = res.cookies.items()
        result['ok'] = res.ok
        result['encoding'] = res.encoding
        # result['raise_for_status()'] = res.raise_for_status()
        result['request_meta'] = res.locust_request_meta
        result['reason'] = res.reason
        result['request'] = req
        result['elapsed'] = res.elapsed.seconds
        return result

        # print(r1.json())
        # print(r1.status_code)
        # print([k+"="+v for k,v in r1.headers.items()])
        # try:
        #     print(r1.request.method)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.url)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.headers)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.files)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.data)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.json)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.params)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(r1.request.auth)
        # except Exception as e:
        #     print(e)
        # try:
        #     print([i for i in r1.request._cookies])
        # except Exception as e:
        #     print(e)

        # print(r1.request)

        # print(r1.json())

        # print(r1.content)
        # print([r1.cookies.items()])
        # print(r1.ok)
        # print(r1.encoding)
        # r1.failure('err')
        # r1.success('ok')

        # print(r1.locust_request_meta)
        # print(r1.raise_for_status())
        # print(r1.text)

        # print(r1.reason)
        # print(r1.elapsed)


RunHttp('http://172.16.32.40:8082', False).add_request('get',
                                                       '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd',
                                                       name='test').run()
# h.add_request('get', '/webapi/api/token/gettoken?openid=f14f531c-2eef-4550-828b-0bdda49ae9dd', name='test')
# # print(**h.run_list[0])
# h.do_http(h.run_dict[h.order_dict['1']])
