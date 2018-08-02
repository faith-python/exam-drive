#!/usr/bin/env python
# -*- coding: utf-8 -*-



from handler.base import BaseRequestHandler

class IndexHandler(BaseRequestHandler):
    def get(self):
        self.render('home/home.html')