#!/usr/bin/env python
# -*- coding: utf-8 -*-



import re
from string import printable

from model.user import UserModel


class CheckArgs():

    user = UserModel

    @classmethod
    def check_argument_reg(cls, username, password1, password2):
        '''
        检查注册传入参数是否有误
        :param username: 手机号码
        :param password1: 输入密码
        :param password2: 重复密码
        :return:True or False
        '''

        if (len(username) == 11) and re.match(r'1\d{10}', username):

            # print('test phone ok!')
            if password1 == password2:
                # print('ok')
                if password1 is None:
                    return False
                else:
                    if 6 < len(password1) < 17:
                        data = [each for each in password1 if each in printable[:94]]
                        # print(data)
                        '''
                        密码只能为英文状态下:
                        0123456789
                        abcdefghijklmnopqrstuvwxyz
                        ABCDEFGHIJKLMNOPQRSTUVWXYZ
                        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
                        '''
                        if len(data) == len(password1):
                            return True
        return False

    @classmethod
    def check_argument_login(self, username, password):
        '''
        检查登录参数
        :param username:
        :param password:
        :return:
        '''
        try:
            int(username)
        except ValueError:
            return False
        if len(username) == 11:
            if 6 <= len(password) <= 16:
                data = [each for each in password if each in printable[:94]]
                if len(data) == len(password):
                    return True
            return False
        else:
            return False



    @classmethod
    def check_user_in_db(cls, username, nickname="", uuid=""):
        '''
        检查登录数据是否存在
        :param username: 手机号
        :param password: 密码
        :param nickname: 昵称
        :return:True or False
        '''

        if cls.user.get_by_username(username):
            return cls.user.get_by_username(username).uuid
        elif cls.user.get_by_nickname(nickname):
            return cls.user.get_by_nickname(nickname).uuid
        elif cls.user.get_by_uuid(uuid):
            return cls.user.get_by_uuid(uuid).uuid

        return False


if __name__ == '__main__':

    '''\
    测试模块是否正常
    '''
    check = CheckArgs()
    test_reg = check.check_register(
        '15885789044', 'ikb234个b254@!', 'ikb234个b254@!')
    print(test_reg)
