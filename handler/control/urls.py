#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.control import questioncontrol
from handler.control import usercontrol

# control url
urls_pattern_control = []


__control_url = [
    # ('/control', control.HomeControlHandler),
]

__question_control_url = [
    ('/control/question/(.*)', questioncontrol.ShowDataHandler),
    ('/json/control/question/(.*)', questioncontrol.GetJsonDataHandler),
    ('/add/control/question/(.*)', questioncontrol.AddquestionHandler),
    ('/del/control/question/(.*)', questioncontrol.DeleteQuestionHandler),
    ('/modify/control/question/(.*)', questioncontrol.ModifyQuestionHandler),

]


__user_control_url = [
    ('/control/user', usercontrol.ShowDataHandler),
    ('/control/user/answer', usercontrol.ShowAnswerHandler),
    ('/control/user/json', usercontrol.GetJsonDataHandler),
    ('/add/control/user', usercontrol.AddUserHandler),
    ('/del/control/user', usercontrol.DeleteUserHandler),
    ('/del/control/user/answer', usercontrol.DeleteScoreHandler),
    ('/modify/control/user', usercontrol.ModifyUserHandler),

]

urls_pattern_control += __control_url
urls_pattern_control += __question_control_url
urls_pattern_control += __user_control_url
