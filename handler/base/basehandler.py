# -*- coding: utf-8 -*-


import json
import redis
import tornado.web
import tornado.websocket
import tornado.escape
import pycket.session

from util.db.db_connect_engine import datebase_session
from model.user import UserModel
from model.carquestion import car_question_factory


from conf import config


def connect_redis_config():
    _conifg_info = config.redis['pycket']['storage']
    result = {
        'host': _conifg_info['host'],
        'port': _conifg_info['port'],
        'db': _conifg_info['db_sessions'],
    }
    return result


redis_connect_pool = redis.ConnectionPool(**connect_redis_config())




class BaseRequestHandler(tornado.web.RequestHandler, pycket.session.SessionMixin):
    '''定义所有handler的基类，用于子handler继承'''

    def prepare(self):
        '''
        重写此方法以执行普通初始化请求的方法.
        ###########-------->>>>>>>>>:异步支持:用“tornado.gen.coroutine”来装饰此方法或“.return_future '使它异步.
        (异步装饰器不能用于“prepare”。)

        :return:
        '''
        '''Called at the beginning of a request before get/post/etc '''
        # ---预解析json
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.load(self.request.body)
        else:
            self.json_args = {}

    def set_default_headers(self):
        """设置默认header"""
        self.set_header("Server", self.request.host)

    def initialize(self):
        '''初始化所有request基类的 默认调用函数'''
        self.dbs = datebase_session
        self.escape = tornado.escape
        self.redis = redis.Redis(connection_pool=redis_connect_pool)


    def get_current_user(self):
        '''
        用户已经登录:
            --返回用户实例
        :return:
            User对象
        '''
        uuid = self.get_secure_cookie('uuid', None)
        if uuid:
            return UserModel.get_by_uuid(uuid)
        return None

    def on_finish(self):
        '''
                重写此方法以执行清理、日志记录等。

                这种方法与“prepare”相对应。“on_finish ' '

                不产生任何输出，因为它是在响应之后调用的

                已发送给客户端。
                :return:
                '''

        # '''断开连接时删除用户cookie'''
        # self.session.delete('uuid')
        pass

    def write_error(self, status_code, **kwargs):

        if status_code == 404:
            self.render('public/404.html')
        elif status_code == 500:
            self.render('public/500.html')
        else:
            super(BaseRequestHandler, self).write_error(status_code, **kwargs)

    # 自定义函数:
    def write_json(self, dict_data):
        self.add_header('Content-Type', 'application/json;charset=utf-8')
        return self.write(tornado.escape.json_encode(dict_data))









class APIBaseHandler(BaseRequestHandler):

    CARTYPE = ['small', 'truck', 'bus', 4]

    def set_default_headers(self):
        """设置默认header"""
        self.set_header("Server", self.request.host)
        self.set_header('Content-Type', 'application/json;charset=utf-8')







class CacheBaseHandler(object):
    '''
    缓存相关操作
    '''
    credis = redis.Redis(connection_pool=redis_connect_pool)

    def cache_get_data_list_len(self, cartype):
        return self.credis.llen(cartype)

    def cache_get_data_list(self, cartype):
        '''
        获取缓存数据 :数据类型 list
        :param cartype:
        :return:
        '''
        cache_list = self.credis.lrange(cartype, 0, -1)
        return cache_list

    def cache_list_lpush(self, cartype, data):
        '''
        新增数据 缓存
        :param cartype:
        :param data:
        :return:
        '''
        return self.credis.lpush(cartype, data)

    def cache_drop_all(self):
        '''
        移除缓存
        :return:
        '''
        self.credis.brpop(self.CARTYPE, timeout=1)

    def cache_write_to(self, cartype):
        '''
        写入数据至缓存
        :param cartype:
        :return:
        '''
        # 检查是否有缓存数据
        cache_list = self.cache_get_data_list(cartype)
        if not cache_list:
            # cache 空:缓存数据
            question_data_cartype = car_question_factory(cartype)
            all_data = question_data_cartype.get_all()
            for each_data in all_data:
                data_info = self.get_question_info(each_data)
                self.cache_list_lpush(cartype, data_info)  # 写入redis缓存

    def cache_get_data_by_id(self, cartype, id):
        '''获取数据
        返回dict对象
        '''
        btmp_id = "'id': {},".format(id).encode('utf8')
        for each in self.cache_get_data_list(cartype):
            if each.find(btmp_id) != -1:
                return self.bytes_to_dict_data(each)

    def bytes_to_dict_data(self, bytes_data):
        '''
        将二进制dict数据 转化为dict对象
        :param bytes_data:
        :return:
        '''
        str_data = bytes_data.decode('utf8').replace("'", '"')
        # print(type(result), result.keys())
        return json.loads(str_data)

    def bytes_to_str(self, bytes_data):
        return bytes_data.decode('utf8')

    def _check_num_to_alph(num):
        '''
        1 ->a
        2 ->b
        3 ->c
        4 _>d
        :return: a/b/c/d
        '''
        num_to_alph = {
            '1': 'a',
            '2': 'b',
            '3': 'c',
            '4': 'd',
        }

        try:
            return num_to_alph[num]
        except KeyError:
            pass

    def __check_question_type(self, *args):
        '''
        检查题库问题选项:
        :param item1: 问题选项

        :return: QTYPE:
            1: 判断题
            2: 单选题
            # 3: 多选择
        '''
        qtype = 0
        for each in args:
            if bool(each):
                qtype += 1
            else:
                return 1
        if qtype == 3 or qtype == 4:
            return 2

    def get_question_info(self, orm_question_data):
        '''
        获取单条数据的信息
        :param orm_question_data:
        :return:
        '''
        ##mysql 字段:
        #
        #
        # '''题库的基类'''
        # id = Column(Integer, autoincrement=True, primary_key=True)
        # uuid = Column(String(32), nullable=False, default=uuid4().hex)
        # qid = Column(Integer, nullable=False, unique=True)
        # answer = Column(String(64), nullable=False, )
        # explains = Column(String(360), )  # 题目详解
        # question = Column(String(220), nullable=False, )  # 问题
        # # subject = Column(String(1), nullable=False, ) #选择考试科目类型，1：科目1；
        # # 4：科目4
        # model = Column(String(2), nullable=True, )  # 驾照类型，可选择参数为：c1,c2,a1,a2,b1,b2；当subject=4时可省略
        # img_url = Column(String(120), nullable=True, )
        # item1 = Column(String(120), nullable=True, )
        # item2 = Column(String(120), nullable=True, )
        # item3 = Column(String(120), nullable=True, )
        # item4 = Column(String(120), nullable=True, )
        # create_time = Column(DateTime, default=datetime.now)
        ###前端对应字段
        # qid = self.get_argument('id', None) 3题目编号
        # question = self.get_argument('question', None)  # 问题叙述
        # bestanswer = self.get_argument('bestanswer', None)  # 答案详解
        # a = self.get_argument('a', None)
        # b = self.get_argument('b', None)
        # c = self.get_argument('c', None)
        # d = self.get_argument('d', None)
        # ta = self.get_argument('ta', None)  # 答案
        # jiazhaoimg = self.get_argument('imageurl', None)

        data_info = {}  # 定义一个获取到信息的dict

        data = orm_question_data
        # 读取信息
        question = data.question
        qid = data.qid
        answer = data.answer
        explains = data.explains
        uid = data.uuid
        img_url = data.img_url
        item1 = data.item1
        item2 = data.item2
        item3 = data.item3
        item4 = data.item4

        # update
        data_info['id'] = qid
        data_info['question'] = question
        data_info['ta'] = answer
        data_info['bestanswer'] = explains
        data_info['jiazhaoimg'] = img_url
        data_info['uuid'] = uid
        data_info['a'] = item1
        data_info['b'] = item2
        data_info['c'] = item3
        data_info['d'] = item4
        data_info['Type'] = self.__check_question_type(item1, item2, item3, item4)

        # print(data_info)
        return data_info


