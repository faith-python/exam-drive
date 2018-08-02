#!/usr/bin/env python
# -*- coding: utf-8 -*-



from handler.base import BaseRequestHandler, APIBaseHandler
from handler.home.lib import CheckArgs
from model.user import UserModel
import libutil

from model.score import SourceModel



class ShowDataHandler(BaseRequestHandler):
    @libutil.check_adminuser
    def get(self):
        user_datas = UserModel.get_all()
        result_data = []
        for user in user_datas:
            if user.locked:
                continue
            result_data.append(user)
        self.render('control/show.html',
                    data= result_data,
                    uri=self.request.uri)


class ShowAnswerHandler(BaseRequestHandler):
    @libutil.check_adminuser
    def get(self):
        user_datas = UserModel.get_all()
        result_data = []
        for user in user_datas:
            if user.locked:
                continue
            #获取对应用户答题数据
            score = SourceModel.get_by_userid(user.id)
            # print(score)
            # print(score[0].score)
            setattr(user, 'source_obj', score)
            result_data.append(user)
        self.render('control/show-answer.html',
                    data=result_data,
                    uri=self.request.uri)



class GetJsonDataHandler(BaseRequestHandler):
    def get(self):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        user_datas = UserModel.get_all()
        for user in user_datas:
            temp_info = {}
            temp_info['id'] = user.id
            temp_info['uuid'] = user.uuid
            temp_info['username'] = user.username
            temp_info['nickname'] = user.nickname
            result_data['data'].append(temp_info)
        self.write_json(result_data)







class AddUserHandler(APIBaseHandler):
    '''
    add new user
    url: /control/user/add
    '''

    def get(self):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        uuid = self.get_argument('uuid', None)
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        nickname = self.get_argument('nickname', None)
        locked = bool(self.get_argument('locked', None))
        if not CheckArgs.check_argument_reg(username, password, password):
            result_data['error_code'] = 400
            result_data['reason'] = '输入非法!'
        if uuid:
            '''有uuid则为修改信息'''
            data_info = UserModel.get_by_uuid(uuid)
            data_info.username = username
            data_info.nickname = nickname
            data_info.password = password
            data_info.locked = locked
        else:
            '''添加用户'''
            data_info = UserModel(
                username= username,
                nickname=nickname,
                password=password,
                locked=locked,
            )
        self.dbs.add(data_info)
        try:
            self.dbs.commit()
        except Exception as e:
            print(e)
            self.dbs.rollback()
            result_data['error_code'] = 400
            result_data['reason'] = '数据提交错误!'
        finally:
            self.dbs.close()
        self.write_json(result_data)









class ModifyUserHandler(BaseRequestHandler):
    '''
    modify user info
    url: /control/user/modify
    '''
    @libutil.check_adminuser
    def get(self,):
        uuid = self.get_argument('uuid', None)
        data = UserModel.get_by_uuid(uuid)
        self.render('control/edit-data.html',
                    data=data,
                    )
from model.score import SourceModel
class DeleteScoreHandler(AddUserHandler):
    def get(self, ):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        uuid = self.get_argument('uuid', None)
        score_data = SourceModel.get_by_uuid(uuid)
        if score_data:
            self.dbs.delete(score_data)
            try:
                self.dbs.commit()
            except Exception as e:
                self.dbs.rollback()
                result_data['error_code'] = 400
                result_data['reason'] = '删除失败'
            finally:
                self.dbs.close()

        self.write_json(result_data)

class DeleteUserHandler(APIBaseHandler):
    '''
    delete user data
    url: /contorl/user/del
    '''

    def get(self, ):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        uuid = self.get_argument('uuid', None)
        user_data = UserModel.get_by_uuid(uuid)
        if user_data:
            user_data.locked = True
            # print(self.dbs.dirty)
            self.dbs.add(user_data)
            try:

                self.dbs.commit()
                # print(user_data.locked)

            except Exception as e:
                print(e)
                self.dbs.rollback()
                result_data['error_code'] = 400
                result_data['reason'] = '删除失败'
            finally:
                self.dbs.close()

        self.write_json(result_data)

