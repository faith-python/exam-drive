#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import tornado.web
from . import error


# 静态路由
urls_pattern_static = [
    # (r"/plugin/(.*)", tornado.web.StaticFileHandler,
    #     {"path": os.path.join(os.path.dirname(__file__).split('handler')[0],
    #                           "static/plugin/")}),
    #     (r"/tmp/(.*)", tornado.web.StaticFileHandler,
    #         {"path": os.path.join(os.path.dirname(__file__).split('handler')[0],
    #                           "static/tmp/")}),

        (r"/public/(.*)", tornado.web.StaticFileHandler,
            {"path": os.path.join(os.path.dirname(__file__).split('handler')[0],
                              "static/public/")}),
]
