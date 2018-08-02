#!/usr/bin/env python
# -*- coding: utf-8 -*-



from handler.home.urls import urls_pattern_home
from handler.public.urls import urls_pattern_static
from handler.api.urls import urls_pattern_api
from handler.control.urls import urls_pattern_control
from handler.drill.urls import urls_pattern_drill
from handler.public.error import PageNotFoundHandler

urls_pattern = []




#api路由
urls_pattern += urls_pattern_api

# home urls
urls_pattern += urls_pattern_home

# 控制路由
urls_pattern += urls_pattern_control

#练习路由
urls_pattern += urls_pattern_drill

#静态路由
urls_pattern += urls_pattern_static

#404  必须最后加载
urls_pattern.append(('.*', PageNotFoundHandler),)
