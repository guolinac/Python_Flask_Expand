"""
 Created by guolin
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token,gift

__author__ = 'guolin'


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    # 红图注册到蓝图上
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    return bp_v1
