#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.api import (get_captcha,
                         ajax)


urls_pattern_api = [
    ('/api/captcha/', get_captcha.CaptchaHandler),
    ('/api/captcha/text/', get_captcha.CaptchaTextHandler),
    ('/api/ajax/getinfo/(.*)/', ajax.AjaxGetInfoHandler),
    ('/api/ajax/order/(.*)/', ajax.AjaxOrderQuestionHandler),
    ('/api/ajax/answer/(.*)/', ajax.ToJsonAnswerHandler),
    ('/api/ajax/saveresult/', ajax.SaveResultHandler),

]
