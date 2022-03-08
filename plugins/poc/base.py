#!/usr/bin/python
# coding=utf-8
'''
Date: 2022-03-04 15:31:48
LastEditors: recar
LastEditTime: 2022-03-08 10:39:33
'''
# from __future__ import absolute_import, unicode_literals

# from http.server import BaseHTTPRequestHandler
# from io import BytesIO
# from urllib import parse

# poc
from requests import sessions
from lib.work import ResultInfo
import requests


requests.packages.urllib3.disable_warnings()

def raw2req(raw):
        CRLF ="\n"
        def _parse_request_line(request_line):
            request_parts = request_line.split(' ')
            method = request_parts[0]
            path = request_parts[1]
            protocol = request_parts[2] if len(request_parts) > 2 else "HTTP 1.1"
            return method, path, protocol

        req_lines = raw.split("\n")
        method, path, protocol = _parse_request_line(req_lines[0])
        ind = 1
        headers = dict()
        while ind < len(req_lines) and len(req_lines[ind]) > 0:
            colon_ind = req_lines[ind].find(':')
            header_key = req_lines[ind][:colon_ind]
            header_value = req_lines[ind][colon_ind + 1:]
            headers[header_key] = header_value.strip()
            ind += 1
        ind += 1
        body = req_lines[ind:] if ind < len(req_lines) else None
        is_json = headers.get('Content-Type')
        if body is not None:
            if is_json=="application/json":
                 body = "".join([b.strip() for b in body])
            else:
                body = CRLF.join(body)
        return method, path, headers, body


def rsp2req_raw(response):
    request = response.request
    http_version_int = response.raw.version
    if http_version_int ==10:
        http_version = "HTTP/1.0"
    else:
        http_version = "HTTP/1.1"
    raw = '%s %s %s\r\n' % (request.method, str(request.path_url), http_version)
    # Add headers to the request
    req_data = ""
    for k, v in request.headers.items():
        req_data += k + ': ' + v + '\r\n'
    req_data += '\r\n'
    req_data += str(request.body)
    return raw    


class PocBase(object):

    def __init__(self,):
        pass
    
    def setup(self):
        ''' 
        测试前准备 比如需要先发几个包去做最后验证的前置条件
        '''
        pass

    def send_payload(self):
        '''
        验证前的最后一个发送请求
        '''
        pass

    def verify(self):
        pass

    def tear_down(self):
        '''
        清理方法 有些poc需要清除前置条件
        '''
        pass

    def request(self, method, url, **kwargs):
        with sessions.Session() as session:
            return session.request(method=method, url=url, **kwargs)

    def get(self, url, params=None, **kwargs):
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, params=params, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends an OPTIONS request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('options', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes. If
            `allow_redirects` is not provided, it will be set to `False` (as
            opposed to the default :meth:`request` behavior).
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', False)
        return self.request('head', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('put', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('patch', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.request('delete', url, **kwargs)

    def send_raw(self, raw):
        # raw_req = RequestParser(raw.encode()).request
        # method = raw_req.method
        # path = raw_req.path
        # headers = raw_req.headers
        # data = raw_req.data
        # params = raw_req.params
        method,path,headers, data = raw2req(raw)
        url = "{0}{1}".format(self.base_url, path)
        tmp = self.request(method, url, headers=headers, data=data, verify=False)
        return tmp


    def run(self, logger, report_work, ip, port, ssl=False):
        # 初始化赋值
        self.logger = logger
        self.report_work = report_work
        self.ip = ip
        self.port = port
        self.ssl = ssl
        self.logger.debug(self.ssl)
        if self.ssl:
            self.base_url = "https://{0}:{1}".format(self.ip, self.port)
        else:
            self.base_url = "http://{0}:{1}".format(self.ip, self.port)
        # 测试流程
        # 前置条件
        self.setup()
        # 发送payload
        response = self.send_payload()
        # 验证
        verify_status = self.verify(response)
        self.logger.debug("{0}  verify_status: {1}".format(self.name, verify_status))
        # 清理环境
        self.tear_down()
        if verify_status:
            self.logger.info("!!!! 发现漏洞: {0} \n{1} \n".format(self.name, response.request.url))
            result_info = ResultInfo(self.name, response.request.url, rsp2req_raw(response), rsp2req_raw(response), "", self.desc)
            self.report_work.put(result_info)