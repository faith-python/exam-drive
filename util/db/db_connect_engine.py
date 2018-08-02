# -*- coding: utf-8 -*-

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from conf.config import db



# engine = create_engine("mysql://scott:tiger@hostname/dbname",encoding='latin1', echo=True)
__config_db = "{}+{}://{}:{}@{}:{}/{}?charset={}".format(
                                                db['datebase'],
                                                db['connector'],
                                                db['user'],
                                                db['passwd'],
                                                db['hostname'],
                                                db['port'],
                                                db['dbname'],
                                                db['charset']
                                            )
db_connect_engine = create_engine(__config_db,
                                  encoding="utf8",
                                  echo=False)
# 创建一个用来继承的基类
Datebase_BaseHandler = declarative_base()
_session = sessionmaker(bind=db_connect_engine)
# 创建DB会话
datebase_session = _session()





