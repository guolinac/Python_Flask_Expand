"""
 Created by guolin
"""
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

__author__ = 'guolin'

app = create_app()


# 捕获所有全局异常，flask1.0版本
@app.errorhandler(Exception)
def framework_error(e):
    """
    AOP思想
    不管未知异常出现在代码的哪个位置，我只需要在程序出口的地方堵住这些异常，然后统一处理即可
    注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法

    捕获处理全局异常的方法有两种：@app.errorhandler、@app.after_request
    1、第一种的使用，需要将flask的debug开关打开才能生效（自动捕获异常），在config里面将DEBUG = TRUE就可以（默认是False）。
    但是，debug模式是万万不建议在生产中开启的，因此，这里这个用法就有所限制了

    2、由于上面第一种方法的巨大局限性（生产不建议开启debug模式），开始考虑第二种方案，想不到很好的方法，
    因此，考虑到用after_request装饰器来统一处理，通过获取请求的response的状态码来做判断，进行统一处理。需要注意的是
    用after_request这种方法需要将debug模式关闭，要不flask自动捕获了异常，装饰器就捕获不到了
    """
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 抛出服务器错误
        if not app.config['DEBUG']:
            return ServerError()
        # 调试模式则打印堆栈的具体信息
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True)
