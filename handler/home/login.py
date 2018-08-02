#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re

from handler.base import BaseRequestHandler
from model.user import UserModel
from .lib import CheckArgs
import libutil

class RegisterHandler(BaseRequestHandler):


    error_message = {
        0: 'ok',
        410: '填写信息错误',
        411: '用户名最多11个字符',
        412: '用户名已经被使用',
        413: '手机号不正确',
        414: '手机号已经被使用',
        415: '注册失败，请稍后再试'
    }

    def get(self):
        self.render('home/reg.html',
                    error=None,
                    )

    def post(self):
        '''注册逻辑判断'''
        username = self.get_argument("username", None)
        password1 = self.get_argument("password1", None)
        password2 = self.get_argument("password2", None)
        nickname = self.get_argument('nickname', None)
        result_data = {
            "error_code": 0,
            "reason": "ok",
            "result": [],
        }
        if CheckArgs.check_argument_reg(username, password1, password2):
            check_db = CheckArgs.check_user_in_db(username=username)
            #检出是否存在用户
            if check_db:
                result_data["error_code"] = 414
                result_data["reason"] = self.error_message[414]
                #self.write(json_data)
            else:
                user = UserModel.new(username, password=password1, nickname=nickname)
            # print('reg:', user)
                if user.uuid:

                    self.clear_all_cookies()
                    self.set_secure_cookie('uuid', user.uuid, expires_days=7)
                    # print(user.uuid)
                else:
                    result_data["error_code"] = 415
                    result_data["reason"] = self.error_message[415]
        else:
            result_data["error_code"] = 410
            result_data["reason"] = self.error_message[410]
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.write_json(result_data)




class LoginHandler(BaseRequestHandler):

    error_message = {
        400: '信息填写不完整',
        401: '该用户不存在',
        402: '密码错误',
        403: '验证码错误'
    }

    def get(self):
        self.render('home/login.html')

    @libutil.check_user_locked
    def post(self):
        '''
        检查用户传入参数,并验证数据库信息
        :return:
        '''
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        result_data = {
            "error_code": 0,
            "reason": "ok",
            "result": [],
        }

        if (not username) or (not password):
            result_data["error_code"] = 400
            result_data["reason"] = self.error_message[400]
        else:
            if CheckArgs.check_argument_login(username, password):
                check_user_data = UserModel.check_user_in_db(username, password)
                if check_user_data:
                    # print(UserModel.get_by_username(username), check_user_data)
                    result_data["error_code"] = 0
                    self.clear_all_cookies()
                    self.set_secure_cookie('uuid', check_user_data.uuid, expires_days=7)
                else:
                    result_data["error_code"] = 400
                    result_data["reason"] = self.error_message[400]
            else:
                result_data["error_code"] = 400
                result_data["reason"] = self.error_message[400]
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.write_json(result_data)




class LogoutHandler(BaseRequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


