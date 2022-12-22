"""
 Created by guolin
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

__author__ = 'guolin'


class ClientForm(Form):
    # 账号     validators是一个验证器，当validate()验证未通过时，会在表单字段下面显示我们传进去的错误提示（例如message= '不允许为空'）
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    # 密码
    secret = StringField()
    # 客户端类型
    type = IntegerField(validators=[DataRequired()])

    # 自定义的验证器
    def validate_type(self, value):
        try:
            # 判断用户传过来的数字是否是枚举类型的一种
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


# 以邮箱方式注册的验证
class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    # 验证账号是否已经被注册过
    def validate_account(self, value):
        # 去数据库里查用户数据是否已经存在
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
