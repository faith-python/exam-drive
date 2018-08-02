#!/usr/bin/env python
# -*- coding: utf-8 -*-



from uuid import uuid4
from datetime import datetime

from sqlalchemy import (Column, Integer, String,
                        Boolean, DateTime,  ForeignKey,
                        Table)
from sqlalchemy.orm import relationship

from util.db.db_connect_engine import (Datebase_BaseHandler,
                                       datebase_session,
                                       db_connect_engine)


def set_uuid():
    return uuid4().hex

class CarQuestionBase(object):
    '''题库的基类'''
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(32), nullable=False, unique=True, default=set_uuid)
    qid = Column(Integer, nullable=True)
    answer = Column(String(64), nullable=False, )
    question = Column(String(220), nullable=False, )  # 问题
    explains = Column(String(360), )  # 题目详解
    img_url = Column(String(120), nullable=True, )
    item1 = Column(String(120), nullable=True, )
    item2 = Column(String(120), nullable=True, )
    item3 = Column(String(120), nullable=True, )
    item4 = Column(String(120), nullable=True, )
    create_time = Column(DateTime, default=datetime.now)
    _locked = Column("locked", Boolean, default=False)

    # 题目锁 1:锁定
    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value:bool):
        # assert isinstance(value, bool)
        self._locked = value

    # 数据库查询引擎
    dbs = datebase_session

    # 定义查询字段
    @classmethod
    def get_all(cls):
        return cls.dbs.query(cls).all()

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.dbs.query(cls). \
            filter_by(uuid=uuid).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.dbs.query(cls).filter_by(id=id).first()

class SmallCarQuestion(Datebase_BaseHandler, CarQuestionBase):
    '''
    小车类型:
        c1, c2
    '''
    __tablename__ = 'itm_smallcar_question'

class TruckCarQuestion(Datebase_BaseHandler, CarQuestionBase):
    '''
    货车类型:
        a2, b2
    '''

    __tablename__ = 'itm_truckcar_question'

class BusCarQuestion(Datebase_BaseHandler, CarQuestionBase):
    '''
    客车类型:
        a1, b1
    '''
    __tablename__ = 'itm_bus_question'


class Car4Question(Datebase_BaseHandler, CarQuestionBase):
    '''
    科目四
    '''
    __tablename__ = 'itm_4_question'


def car_question_factory(cartype):
    _data = {
        'small': SmallCarQuestion,
        'truck': TruckCarQuestion,
        'bus': BusCarQuestion,
        '4': Car4Question,
    }

    if cartype == 'small':
        return _data['small']
    elif cartype == 'truck':
        return _data['truck']
    elif cartype == 'bus':
        return _data['bus']
    elif cartype == '4':
        return _data['4']
    else:
        raise KeyError('no {} question type table!!!'.format(cartype))
