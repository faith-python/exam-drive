#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.drill import drill


urls_pattern_drill = [
    (r'/drill/(.*)/(.*)/', drill.IndexHandler),

]