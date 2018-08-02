#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from model.carquestion import car_question_factory
from util.capture.api import api_exam
from util.db import datebase_session

        

class SaveQuestionData(object):
    questiontype = ['small', 'truck', 'bus', '4']
    alltype = {
        'small': ['c1', 'c2'],
        'truck': ['a2', 'b2'],
        'bus': ['a1', 'b1'],
        '4': ['4'],
    }  # 所有驾照类型
    def __init__(self, cartype):
        self._cartype = cartype
        
    
    def _to_save_data(self, data_obj, cartype_db):
        '''
        :param data_dict: 待保存的数据对象
        :param cartype_db: 将要保存到的数据库对象
        :return:
        '''
        qid = data_obj['id']
        question = data_obj['question']
        answer = data_obj['answer']
        explains = data_obj['explains']
        img_url = data_obj['url']

        item1 = data_obj['item1']
        item2 = data_obj['item2']
        item3 = data_obj['item3']
        item4 = data_obj['item4']

        # -------保存数据库------
        for_save_data = cartype_db(
            qid=qid,
            answer=answer,
            explains=explains,
            question=question,
            img_url=img_url,
            item1=item1,
            item2=item2,
            item3=item3,
            item4=item4,
        )
        datebase_session.add(for_save_data)
        try:
            datebase_session.commit()
            print('正在保存数据', for_save_data)
        except Exception as e:
            print('数据已存在:已将跳过!',e)
            datebase_session.rollback()


    def load_data(self, remote_data, cartype):
        '''
        保存数据
        :param remote_data:
        :param cartype:
        :return:
        '''
        json_data = json.loads(remote_data)
        for each_data in json_data:
            self._to_save_data(each_data, cartype)


    def save_to_database(self):
        if self._cartype in self.questiontype:
            if  not car_question_factory(self._cartype).get_all():
                if self._cartype == 'small':
                        for eachtype in self.alltype['small']:
                            small_car = car_question_factory(self._cartype) #小车类型(数据库)
                            remote_data = api_exam.exam(1, model=eachtype, testType='order')
                            self.load_data(remote_data, small_car)
                elif self._cartype == 'truck':
                    for eachtype in self.alltype['truck']:
                        truck_car = car_question_factory(self._cartype) #货车类型
                        remote_data = api_exam.exam(1, model=eachtype, testType='order')
                        self.load_data(remote_data, truck_car)
                elif self._cartype == 'bus':
                    for eachtype in self.alltype['bus']:
                        bus_car = car_question_factory(self._cartype) # 客车类型
                        remote_data = api_exam.exam(1, model=eachtype, testType='order')
                        self.load_data(remote_data, bus_car)

                elif self._cartype == '4':
                    for eachtype in self.alltype['4']:
                        car4 = car_question_factory(self._cartype) # 科目四
                        remote_data = api_exam.exam(4,model=4 ,testType='order')
                        self.load_data(remote_data, car4)
            else:
                print('已初始化数据库!!!请清空数据库...')

            datebase_session.close()




    
if __name__ == '__main__':
    SaveQuestionData('small').save_to_database()
    SaveQuestionData('truck').save_to_database()
    SaveQuestionData('bus').save_to_database()
    SaveQuestionData('4').save_to_database() #科目4题库