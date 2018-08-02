
import random
from handler.base import BaseRequestHandler
from model.carquestion import car_question_factory
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


def car_question_cache_factory(cartype):
    _CARTYPE = {
        'small': SMALL_CAR_CACHE,
        'truck': TRUCK_CAR_CACHE,
        'bus': BUS_CAR_CACHE,
        '4': CAR_CACHE_4,
    }
    if cartype == 'small':
        return _CARTYPE['small']
    elif cartype == 'truck':
        return _CARTYPE['truck']
    elif cartype == 'bus':
        return _CARTYPE['bus']
    elif cartype == '4':
        return _CARTYPE['4']
    else:
        raise KeyError('no {} type cache!!! palese check!!!'.format(cartype))

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

def __check_question_type(*args):
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




def get_question_info(orm_question_data):
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
    # qid = self.get_argument('id', None)
    # question = self.get_argument('question', None)  # 问题叙述
    # bestanswer = self.get_argument('bestanswer', None)  # 答案详解
    # a = self.get_argument('a', None)
    # b = self.get_argument('b', None)
    # c = self.get_argument('c', None)
    # d = self.get_argument('d', None)
    # ta = self.get_argument('ta', None)  # 答案
    # jiazhaoimg = self.get_argument('imageurl', None)


    data_info = {} #定义一个获取到信息的dict

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
    data_info['ta'] =answer
    data_info['bestanswer'] = explains
    data_info['jiazhaoimg'] = img_url
    data_info['uuid'] = uid
    data_info['a'] = item1
    data_info['b'] = item2
    data_info['c'] = item3
    data_info['d'] = item4
    data_info['Type'] = __check_question_type(item1, item2, item3, item4)

    # print(data_info)
    return data_info




class AjaxGetInfoHandler(BaseRequestHandler):
    '''
    ajax请求数据
    URL:
    eg:
        /api/ajax/getinfo/small/?id=400

        return:
        {
    "status":true,
    "data":{
        "id":"400",
        "question":"驾驶机动车向右变更车道前应仔细观察右侧车道车流情况的原因是什么?",
        "a":"准备抢行",
        "b":"判断有无变更车道的条件",
        "c":"迅速变更车道",
        "d":"准备迅速停车",
        "ta":"2",
        "bestanswer":"观察当然是为了判断有无变更车道的条件了。",
        "Type":"2",
        "jiazhaoimg":null
    }
}

    '''


    def get(self, cartype):
        '''

        :param cartype: c参数:small, truck, bus, 4
        :return: json data
        '''
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        try:
            # 捕获题库查询错误异常
            question_data_cartype = car_question_factory(cartype)
        except KeyError as e:
            result_data = {
                'error_code': 40001,
                'msg': '获取数据失败',
                'data': [],
            }
            # print(e)
            self.write_json(result_data)
        else:
            qid = self.get_argument('id', None)
            try:
                int(qid)
            except (ValueError,TypeError) as e:
                result_data = {
                    'error_code': 40001,
                    'msg': '获取数据失败',
                    'data': [],
                }
                # print(e)
                self.write_json(result_data)
            else:
                self.set_header('Content-Type', 'application/json;charset=utf-8')
                data = question_data_cartype.get_by_id(qid)
                if data:
                    data_info = get_question_info(data)
                    result_data['data'] = data_info
                    self.write_json(result_data)
                else:
                    result_data = {
                        'error_code': 40001,
                        'msg': '获取数据失败',
                        'data': [],
                    }
                    # print(e)
                    self.write_json(result_data)



class AjaxOrderQuestionHandler(BaseRequestHandler):
    '''
    获取所有题目信息
    首次访问:加载数据至缓存
    '''
    CARTYPE = ['small', 'truck', 'bus', 4]
    def get(self, cartype):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        if cartype in self.CARTYPE:
            #检查是否有缓存数据
            cache_list = car_question_cache_factory(cartype)
            if not cache_list:
                # cache 空:缓存数据
                question_data_cartype = car_question_factory(cartype)
                all_data = question_data_cartype.get_all()
                for each_data in all_data:
                    data_info = get_question_info(each_data)
                    cache_list.append(data_info)
            result_data['data'].extend(cache_list)
            self.set_header('Content-Type', 'application/json;charset=utf-8')
            self.write_json(result_data)
    post = get





class ToJsonAnswerHandler(BaseRequestHandler):
    '''
    顺序抽题
    '''
    CARTYPE = ['small', 'truck', 'bus', '4']
    def get(self, cartype):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        if cartype in self.CARTYPE:
            # 检查是否有缓存数据
            cache_list = car_question_cache_factory(cartype)
            if not cache_list:
                # cache 空:缓存数据
                question_data_cartype = car_question_factory(cartype)
                all_data = question_data_cartype.get_all()
                for each_data in all_data:
                    data_info = get_question_info(each_data)
                    cache_list.append(data_info)
            cache_list = car_question_cache_factory(cartype)


            for data in cache_list:
                data_info = {}
                data_info["id"] = data['id']
                data_info["ta"] = data['ta']
                data_info["Type"] = data['Type']
                result_data['data'].append(data_info)
        self.write_json(result_data)

    post=get




class SaveResultHandler(BaseRequestHandler):
    '''
    保存用户答题信息
    '''

    @libutil.source_to_db
    def get(self):
        result_data = {
            'error_code': 0,
            'reason': 'ok',
            'data': [],
        }
        score = self.get_argument('score') #总分
        rightnum = self.get_argument('rightNum', None) # 答对数目
        wrongnum = self.get_argument('wrongNum', None) # 答错数目
        loudanum = self.get_argument('loudaNum', None) # 漏答数目
        # txtype = self.get_argument('txtype', None)
        # kmtype = self.get_argument('kmtype', None)
        yongshi = self.get_argument('yongshi', None)
        nickname = self.get_argument('nickname', None)
        try:
            int(score) and int(rightnum) and int(wrongnum)
        except Exception as e:
            result_data['error_code'] = 400
            result_data['reason'] = '系统错误!'
            print(e)
        else:
            score = int(score)
            rightnum = int(rightnum)
            wrongnum = int(wrongnum)
            get_grade = self.grade(score, rightnum + wrongnum)
            # print(get_grade)
            result_data['reason'] = get_grade
            result_data['data'].append(rightnum)
        self.write_json(result_data)






    def grade(self, score, total):
        '''

        :param score: 正确的
        :param total: 总共的
        :return: 评分等级
        '''
        result = ''
        if total: #判断是否有参数传入
            try:
                int(score)
            except (ValueError, TypeError) as e:
                print(ValueError('参数错误!!!{name}',format(self.__class__)))
            else:
                try:
                    this_grade = int(score)
                except Exception as e:
                    pass
                else:
                    if (0 <= this_grade < 90) or (this_grade == None):
                        result = '不合格'
                    elif 90 <= this_grade <= 100:
                        result = '合格'
        else:# 没有参数传入
            result = '还没答题呢!!!'
        return result






