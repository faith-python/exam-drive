#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from handler.base import BaseRequestHandler, APIBaseHandler
from model.carquestion import car_question_factory
from handler.api.ajax import car_question_cache_factory, get_question_info
import libutil

#缓存数据
#小车
SMALL_CAR_CACHE = []
#货车
TRUCK_CAR_CACHE = []
#客车
BUS_CAR_CACHE = []
#科目4
CAR_CACHE_4 = []


class ShowDataHandler(BaseRequestHandler):
    '''
    展现数据
    '''
    # CARTYPE = ['small', 'truck', 'bus', 4]
    @libutil.check_adminuser
    @libutil.check_cartye
    def get(self, cartype):
        # print(self.current_user)

        all_data = car_question_factory(cartype).get_all()
        result_data = []

        for data in all_data:
            if data.locked:
                continue
            result_data.append(data)
            # print(result_data)
        self.render('control/show.html',
                    data= result_data,
                    uri=self.request.uri)

class GetJsonDataHandler(BaseRequestHandler):
    '''
    返回题目信息
    '''
    @libutil.check_cartye
    def get(self, cartype):

        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        cache_list = car_question_cache_factory(cartype)
        if not cache_list:
            all_data = car_question_factory(cartype).get_all()
            if len(all_data) != len(cache_list):
                #缓存数据与后台数据不同一,则更新缓存
                for question in all_data:
                    temp = {}
                    temp["id"] = question.qid
                    temp["uuid"] = question.uuid
                    temp["question"] = question.question
                    temp["answer"] = question.answer
                    temp["explains"] = question.explains
                    temp["a"] = question.item1
                    temp["b"] = question.item2
                    temp["c"] = question.item3
                    temp["d"] = question.item4
                    temp["img"] = question.img_url
                    cache_list.append(temp)

        result_data['data'].extend(cache_list)
        self.write_json(result_data)





class AddquestionHandler(APIBaseHandler):
    '''
    新增题库信息
    url: /control/quesiotn/add/item(数据库表)
    '''
    @libutil.check_cartye
    def get(self, cartype):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        #qid = self.get_argument('id', None)
        uuid = self.get_argument('uuid', None)
        question = self.get_argument('question', None)  # 问题叙述
        bestanswer = self.get_argument('bestanswer', None)  # 答案详解
        a = self.get_argument('a', None)
        b = self.get_argument('b', None)
        c = self.get_argument('c', None)
        d = self.get_argument('d', None)
        ta = self.get_argument('ta', None)  # 答案
        imageurl = self.get_argument('img', None)
        locked = bool(self.get_argument('locked', None))

        cartype_orm = car_question_factory(cartype)
        if uuid:
            '''传入uuid则为修改数据'''
            data_info = cartype_orm.get_by_uuid(uuid)
            #data_info.qid = qid
            data_info.question = question
            data_info.explains = bestanswer
            data_info.answer = ta
            data_info.img_url = imageurl
            data_info.item1 = a
            data_info.item2 = b
            data_info.item3 = c
            data_info.item4 = d
            data_info.locked = locked
        else:
            '''添加数据'''
            data_info = cartype_orm(
                                    #qid=qid,
                                    question=question,
                                    explains=bestanswer,
                                    item1=a,
                                    item2=b,
                                    item3=c,
                                    item4=d,
                                    answer=ta,
                                    img_url=imageurl,
                                    locked=locked
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



class ModifyQuestionHandler(BaseRequestHandler):
    '''
    修改题库数据
    url: /control/question/modify/item..
    '''

    @libutil.check_adminuser
    @libutil.check_cartye
    def get(self, cartype):
        uuid = self.get_argument('uuid', None)
        data = car_question_factory(cartype).get_by_uuid(uuid)

        # print(data, uuid)
        self.render('control/edit-data.html',
                    data=data,
                    )

class DeleteQuestionHandler(APIBaseHandler):
    '''
    删除问题数据
    url: /control/question/del/itemname
    '''
    @libutil.check_cartye
    def get(self, cartype):
        # print(cartype)
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        uuid = self.get_argument('uuid', None)

        for_del_data = car_question_factory(cartype).\
                                    get_by_uuid(uuid)
        # print(uuid, for_del_data.locked, for_del_data)
        if for_del_data:
            for_del_data.locked = True
            self.dbs.add(for_del_data)
            try:
                self.dbs.commit()  # 删除问题数据
            except Exception as e:
                print(e)
                self.dbs.rollback()
                result_data['error_code'] = 400
                result_data['reason'] = '删除失败'
            finally:
                self.dbs.close()
        self.write_json(result_data)


