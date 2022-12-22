"""
 Created by guolin
"""

__author__ = 'guolin'


class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    # 实现装饰器，也就是视图函数的@api.route('/xxx')
    # **options可变长参数，传列表
    # 1、*参数收集所有未匹配的位置参数组成一个tuple对象
    # 2、**参数收集所有未匹配的关键字参数组成一个dict对象
    def route(self, rule, **options):
        # f 就是装饰器所作用的方法
        def decorator(f):
            # 把f, rule, options先存到列表里
            self.mound.append((f, rule, options))
            return f

        return decorator

    # 注册到蓝图上
    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        # 序列自动解包
        for f, rule, options in self.mound:
            # options是一个字典，options.pop("endpoint", f.__name__)就是取出字典中key为"endpoint"的value
            # 如果没有这个key，则会把函数的名字作为value取出来
            endpoint = self.name + '+' + \
                       options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
