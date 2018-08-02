#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
from handler.base import BaseRequestHandler
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

class IndexHandler(BaseRequestHandler):
    '''
    返回页面首页
    '''
    SHOWTYPE = ['order', 'random']
    @libutil.check_cartye
    def get(self, cartype, showtype):
        if not showtype:
            self.render('home/home.html')
        elif showtype == 'order':
            self.render('drill/order.html')
        elif showtype == 'random':
            self.render('drill/random.html',
                        user=self.current_user,
                        showtime=False,
                        showalert=False)
        elif showtype == 'exam':
            self.render('drill/random.html',
                        user=self.current_user,
                        showtime=True,
                        showalert=True)

    @libutil.check_cartye
    def post(self, cartype, showtype):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }

        # 检查是否有缓存数据
        cache_list = car_question_cache_factory(cartype)
        if not cache_list:
            # cache 空:缓存数据
            question_data_cartype = car_question_factory(cartype)
            all_data = question_data_cartype.get_all()
            for each_data in all_data:
                data_info = get_question_info(each_data)
                cache_list.append(data_info)



        data_info_list = self.get_data_info_list(cache_list,
                                                 type=showtype)
        result_data['data'].extend(data_info_list)
        # print(cache_list)
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.write_json(result_data)




    def get_data_info_list(self, cache_list, type='order') ->list:
        '''
        获取答案详情
        :param data:
        :return: list
        '''
        tmp_list = []
        if type == 'order':
            for data in cache_list:
                data_info = {}
                data_info['id'] = data['id']
                data_info['ta'] = data['ta']
                data_info['Type'] = data['Type']
                tmp_list.append(data_info)
        elif type == 'random':
            for data in random.sample(cache_list, 100):
                data_info = {}
                data_info['id'] = data['id']
                data_info['ta'] = data['ta']
                data_info['Type'] = data['Type']
                tmp_list.append(data_info)
        return tmp_list
