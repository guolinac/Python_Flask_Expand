"""
 Created by guolin
 自定义错误机制，返回json格式的错误给前端
 重写一些HTTPException的一些异常处理机制
"""
from flask import request, json
from werkzeug.exceptions import HTTPException

__author__ = 'guolin'


class APIException(HTTPException):
    # 默认是未知错误
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999

    # 构造函数可以改变默认值
    # headers是http头信息
    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    # 重写get_body方法，json序列化
    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            # request就是url信息，让前端知道是哪个接口出现异常
            request=request.method + ' ' + self.get_url_no_param()
        )
        # 转Json
        text = json.dumps(body)
        return text

    # 控制返回的http头为json
    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json; charset=utf-8"')]

    # url去掉问号之后的参数
    @staticmethod
    def get_url_no_param():
        # request.full_path是完整url的路径
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

