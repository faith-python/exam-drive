#!/usr/bin/env python
# -*- coding: utf-8 -*-


from handler.base import BaseRequestHandler
from util.verify.sms import Sendsms
from util.verify.captcha import Captcha
from util.verify.sms import Sendsms


class CaptchaHandler(BaseRequestHandler):
    '''
    验证码处理,验证码
    '''

    def get(self):
        '''
        返回验证码信息
        :return:
        '''
        # result_data = {
        #     'error_code': 400,
        #     'reason': '请输入正确的手机号!',
        #     'result': [],
        # }
        username = self.get_argument('username', None)
        try:
            int(username)
        except (ValueError, TypeError) as e:
            # self.write_json(result_data)
            pass
        else:
            if len(username) != 11:
               # self.write_json(result_data)
                pass
            else:
                captcha_text, buffer = Captcha().get_text_buffer
                # print(captcha_text)
                #获取验证码并储存redis
                self.set_header('Content-type', 'image/jpg')
                self.set_header('Content-length', len(buffer))
                redis_save_name = 'captcha:' + username
                # print(redis_save_name)
                #储存redis以便验证码
                self.session.set(redis_save_name, captcha_text.lower()) # 将验证码转换为小写字符
                #发送验证码 --> 手机号
                #sms = Sendsms(moblie, param=captcha_text)
                #sms.send_sms
                self.write(buffer)

    def post(self):
        result_data = {
            'error_code': 400,
            'reason': '请输入正确的手机号!',
            'result': [],
        }
        captcha = self.get_argument('captcha', None)
        username = self.get_argument('username', None)
        try:
            redis_save_name = 'captcha:' + username
        except TypeError as e:
            print(e)

            self.write_json(result_data)
        else:
            if self.session.get(redis_save_name) == captcha:
                result_data['error_code'] = 0
                result_data['reason'] = 'ok'
                self.set_header('Content-Type', 'application/json;charset=utf-8')
                self.write_json(result_data)

class CaptchaTextHandler(BaseRequestHandler):
    '''
    获取文本验证码
    '''
    def post(self):
        result_data = {
            'error_code': 400,
            'reason': '请输入正确的手机号!',
            'result': [],
        }
        username = self.get_argument('username', None)
        try:
            int(username)
        except (ValueError, TypeError) as e:
            # self.write_json(result_data)
            pass
        else:
            if len(username) != 11:
                # self.write_json(result_data)
                pass
            else:
                text_redis_name = 'captcha:' + username
                data = self.session.get(text_redis_name)
                result_data['error_code'] = 0
                result_data['reason'] = data
                #Content-Type:application/json;charset=utf-8
                self.set_header('Content-Type',  'application/json;charset=utf-8')
                self.write_json(result_data)



