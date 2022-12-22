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
