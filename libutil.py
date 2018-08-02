#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
装饰器模块:
    处理参数检验
'''
import tornado.escape
from model.user import UserModel

def _write_error(self,  error_type):
    '''
    返回错误
    :param self:
    :param result_data:
    :param error_type:
    :return:
    '''
    result_data = {
        'error_code': 0,
        'reason': 'ok',
        'data': [],
    }
    result_data['error_code'] = 4000
    result_data['reason'] = 'not {} type!'.format(error_type)
    self.write(tornado.escape.json_encode(result_data))

def check_cartye(handler_method_func):
    '''
    检查车型
    :param handler_method_func: handler: get/post etc.
    :return: func
    '''
    all_cartype = ('small', 'truck', 'bus', '4')
    def wrapper(*args, **kwargs):
        self = args[0]
        cartype = args[1].split('/')[0]
        if cartype in all_cartype:
            return handler_method_func(*args, **kwargs)
        else:
            # 没有该车型, 返回json data 错误
            _write_error(self, cartype)
    return wrapper


def check_showtype(handler_method_func):
    '''
    检查显示形式: order/random
    :param handler_method_func: handler: get/post etc.
    :return: func
    '''
    all_showtype = ('order', 'random')
    def wrapper(*args, **kwargs):
        self = args[0]
        if len(args) >2:
            showtype = args[2]
            if showtype in all_showtype:
                return handler_method_func(*args, **kwargs)
            else:
                _write_error(self,  showtype)
    return wrapper




def check_adminuser(handler_method_func):
    def wrapper(*args, **kwargs):
        self =  args[0] #该url处理器本身
        if self.current_user:
            if UserModel.get_by_uuid(self.current_user.uuid).id == 1:
                return handler_method_func(*args, **kwargs)
        # self.write('not admin user!!!')
        self.redirect('/')
    return wrapper



def check_user_locked(handler_method_func):
    def wrapper(*args, **kwargs):
        result_data = {
            "error_code": 0,
            "reason": "ok",
            "result": [],
        }
        self = args[0]  # 该url处理器本身
        username = self.get_argument('username')

        user = UserModel.get_by_username(username)
        # print(username, user)
        if hasattr(user, 'locked'):
            if not user.locked: # 用户没有锁定
                return handler_method_func(*args, **kwargs)

            result_data["error_code"] = 400
            result_data["reason"] = '该用户已锁定!!!!'

        else: # 查询没有该用户 (None)
            result_data['error_code'] = 400
            result_data['reason'] = '该用户不存在!!!'

        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.write_json(result_data)

    return wrapper





#保存分数数据至数据库
from model.score import SourceModel
from model.user import UserModel
def source_to_db(handler):
    def wrapper(*args, **kwargs):
        self = args[0]
        score = self.get_argument('score', None)  # 总分
        rightnum = self.get_argument('rightNum', None)  # 答对数目
        wrongnum = self.get_argument('wrongNum', None)  # 答错数目
        loudanum = self.get_argument('loudaNum', None)  # 漏答数目


        #判断用户是否登录
        # print(self.current_user.uuid)
        if self.current_user:
            user_id = UserModel.get_by_uuid(self.current_user.uuid).id


            save_source = SourceModel(score=score,
                                      rightnum=rightnum,
                                      wrongnum=wrongnum,
                                      loudanum=loudanum,
                                      user_id=user_id)
            self.dbs.add(save_source)
            try:
                self.dbs.commit()
            except Exception as e:
                self.dbs.rollback()


        return handler(*args, **kwargs)

    return wrapper