"""
 Created by guolin
"""
from flask import request, jsonify

from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException

__author__ = 'guolin'

api = Redprint('client')


# 注册
@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    # 以字典的方式，处理不同客户端的注册代码
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()


# 通过邮箱注册
def __register_user_by_email():
    # 验证
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)
