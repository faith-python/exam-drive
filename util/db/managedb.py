# -*- coding: utf-8 -*-


from .db_connect_engine import Datebase_BaseHandler, db_connect_engine



def create_all():
    '''
    创建数据库表及其字段
    :return:
    '''
    Datebase_BaseHandler.metadata.create_all(bind=db_connect_engine)

def drop_all():
    '''
    删除数据库表及其字段
    :return:
    '''
    Datebase_BaseHandler.metadata.drop_all(bind=db_connect_engine)



