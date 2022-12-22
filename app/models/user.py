"""
 Created by guolin
"""
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

__author__ = 'guolin'


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    # 权限标识，1为普通用户，2为管理员
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(500))

    def keys(self):
        return ['id', 'email', 'nickname', 'auth']

    # @property装饰器会将方法转换为相同名称的只读属性，可以与所定义的属性配合使用，这样可以防止属性被修改
    @property
    def password(self):
        return self._password

    # @password.setter设置密码
    @password.setter
    def password(self, raw):
        # hash加密
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        # 使用 with 关键字系统会自动调用 f.close() 方法， with 的作用等效于 try/finally 语句是一样的
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        # 先查询是否有当前账号
        user = User.query.filter_by(email=email).first_or_404()
        # 比对用户输入的密码和数据库的密码是否一致
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        # 看原始密码和数据库中的密码加密后是否相等
        return check_password_hash(self._password, raw)

    # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']
