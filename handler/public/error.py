#!/usr/bin/env python
# -*- coding: utf-8 -*-



from handler.base import BaseRequestHandler

class PageNotFoundHandler(BaseRequestHandler):
    def get(self):
        self.render('public/404.html')
        print(self.get_status())
    def write_error(self, status_code, **kwargs):
        self.render('public/404.html')