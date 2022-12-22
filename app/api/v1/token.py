"""
 Created by guolin
"""
from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature

api = Redprint('token')

__author__ = 'guolin'


# 登录其实就是获取token的操作
@api.route('', methods=['POST'])
def get_token():
    # 验证
    form = ClientForm().validate_for_api()
    # 字典，根据对应的数字码，区分不同客户端的类型
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    # 密码的验证，也就是执行User.verify()方法
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # 如果上方校验通过，则这里生成Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    # 用序列化器生成的token是byte类型的，要把它转为str
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)


# uid，ac_type客户端类型，scope权限作用域，expiration过期时间
def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    # 生成令牌，SECRET_KEY是加salt
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    # 令牌序列化
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
