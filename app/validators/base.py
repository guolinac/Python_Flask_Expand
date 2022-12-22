"""
 Created by guolin
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException

__author__ = 'guolin'


# 改写WTForms的行为
class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        # 调用父类的构造函数
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # 错误信息是存在form的errors中的
            raise ParameterException(msg=self.errors)
        # 返回form本身
        return self
