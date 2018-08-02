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

from util.db import create_all

class SourceModel(Datebase_BaseHandler):
    '''
    保存用户做题分数
    '''

    __tablename__ = 'itm_source'

    uuid = Column(String(32), nullable=False, unique=True, default=lambda : uuid4().hex)
    id = Column(Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    score = Column(Integer, )
    rightnum = Column(Integer) #总分
    wrongnum = Column(Integer) #答错题数
    loudanum = Column(Integer) #楼答题数

    user_id = Column(Integer)

    sdb = datebase_session



    #定义查询函数
    @classmethod
    def get_by_userid(cls, user_id):
        return cls.sdb.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.sdb.query(cls).filter_by(uuid=uuid).first()



if __name__ == '__main__':
    create_all()