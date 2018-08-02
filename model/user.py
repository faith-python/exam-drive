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
import hashlib


_SALT = 'tornado_dubug_salt'

def set_uuid():
    return uuid4().hex

class UserModel(Datebase_BaseHandler):
    '''user model'''

    __tablename__ = "itm_user"
    dbs = datebase_session

    id = Column(Integer, unique=True, nullable=False, autoincrement=True, primary_key=True)
    uuid = Column(String(32), nullable=False,unique=True, default=set_uuid)
    username = Column(String(20), nullable=False, unique=True,)
    _password = Column("password", String(32), nullable=False)
    nickname = Column(String(20), )
    email = Column(String(20), nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    login_num = Column(Integer, )
    last_login_time = Column(DateTime)
    last_login_ip = Column(String(16))
    role_id = Column(Integer)
    _locked = Column("locked", Boolean, default=False)


    def __init__(self, username, password,
                 nickname=None,locked=False, email=None, update_time=datetime.now):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.email = email
        self.locked = locked



    def __repr__(self):
        return "<UserModel(name='%s', nickname='%s', password: %s, uuid='%s', locked='%s')>" % (
            self.username, self.nickname, self._password, self.uuid, self.locked)


    @classmethod
    def new(cls, username, password, nickname=None, email=None):
        '''
        添加用户
        :param username:
        :param password:
        :param nickname:
        :param email:
        :return:
        '''
        user = UserModel(username=username,
                         password=password,
                         nickname=nickname,
                         email=email)
        cls.dbs.add(user)
        # 只有提交事务了，才可以获取(user.id)数据的ID值
        #捕获异常
        try:
            cls.dbs.commit()
        except:
            cls.dbs.rollback()
        # print(user)
        # print(cls.get_by_username(username))
        if user:
            print('new:', user)
            # return cls.get_by_username(username)
            return user
        return None

    # @classmethod
    # def update_password(cls, password):
    #     '''
    #     更新密码
    #     :param password:
    #     :return:
    #     '''
    #     password = cls._hash_password(password)
    #     update_time = datetime.now()
    #     update = {
    #         cls.password: password,
    #         cls.update_time: update_time,
    #     }
    #     cls.dbs.query(cls).filter_by(id=cls.id).update(update)
    #     try:
    #         cls.dbs.commit()
    #     except:
    #         cls.rollback()


    # @classmethod
    # def update_login_info(cls, last_login_ip):
    #     '''
    #     更新登录信息
    #     :param last_login_ip:
    #     :return:
    #     '''
    #     current_time = datetime.now()
    #     last_login_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #     update = {
    #         cls.last_login_time: last_login_time,
    #         cls.last_login_ip: last_login_ip,
    #         cls.login_num: cls.login_num + 1
    #     }
    #     cls.dbs.query(cls).filter(cls.user_id == cls.user_id).update(update)
    #     try:
    #         return cls.dbs.commit()
    #     except:
    #         cls.dbs.rollback()

    # @classmethod
    # def update_email(cls, email):
    #     '''
    #     更新邮箱
    #     :param email:
    #     :return:
    #     '''
    #     current_time = datetime.now()
    #     update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #     update = {
    #         cls.email: email,
    #         cls.update_time: update_time
    #     }
    #     cls.dbs.query(cls).filter(cls.user_id == cls.user_id).update(update)
    #     try:
    #         return cls.dbs.commit()
    #     except:
    #         cls.dbs.rollback()
    #
    # @classmethod
    # def update_nickname(cls, nickname):
    #     '''
    #     更新昵称
    #     :param nickname:
    #     :return:
    #     '''
    #     current_time = datetime.now()
    #     update_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    #     update = {
    #         cls.nickname: nickname,
    #         cls.update_time: update_time
    #     }
    #     cls.dbs.query(cls).filter(cls.user_id == cls.user_id).update(update)
    #     try:
    #         return cls.dbs.commit()
    #     except:
    #         cls.dbs.rollback()

    @classmethod
    def check_user_in_db(cls, username, password):
        user = cls.get_by_username(username)
        if user:
            if user.check_password(password):
                return user
        return False

    # 方法转属性
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    # hash password
    def _hash_password(self, password):
        # return PBKDF2.crypt(_SALT + password, iterations=0x2537)
        hashof_str = _SALT + password
        return hashlib.md5(hashof_str.encode('utf-8')).hexdigest()

    def check_password(self, other_password):
        '''验证密码'''

        hashof_str = _SALT + other_password
        # print('hash:',self._hash_password('123456a'))
        # print('check:',hashlib.md5(hashof_str.encode('utf-8')).hexdigest())
        if self.password == hashlib.md5(hashof_str.encode('utf-8')).hexdigest():
            return True
        return False

    # 账户锁
    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    # 定义查询字段
    @classmethod
    def get_all(cls):
        return cls.dbs.query(cls).all()

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.dbs.query(cls).\
            filter_by(uuid=uuid).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.dbs.query(cls).\
            filter_by(username=username).first()

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.dbs.query(cls). \
            filter_by(nickname=nickname).first()

    @classmethod
    def get_count(cls):
        return cls.dbs.query(cls).count()



#
# class UserRoleModel(Datebase_BaseHandler):
#     __tablename__ = 'itm_user_role'
#
#     role_id = Column(Integer, primary_key=True)
#     role_name = Column(String(20))
#     description = Column(String(660))
#     list_order = Column(Integer)
#     status = Column(Integer)
#
#     def __init__(self, role_id, role_name, description, list_order, status):
#         self.role_id = role_id
#         self.role_name = role_name
#         self.description = description
#         self.list_order = list_order
#         self.status = status
#
#     def __repr__(self):
#         return "<UserRole('%s')>" % self.role_name
#
#     @classmethod
#     def initialize(cls, item):
#         if not item:
#             return None
#         role_id = item.role_id
#         role_name = item.role_name
#         description = item.description
#         list_order = item.list_order
#         status = item.status
#         if not role_id:
#             return None
#         return cls(role_id, role_name, description, list_order, status)
#
#     @classmethod
#     def new(cls, role_name, description, list_order, status):
#         """
#         add new role
#         """
#         role = UserRoleModel(None, role_name, description, list_order, status)
#
#         cls.dbs.add(role)
#         try:
#             cls.dbs.commit()
#             return True
#         except:
#             cls.dbs.rollback()
#             return None
#
#     @classmethod
#     def update(cls, role_id, role_name, description, list_order, status):
#         update = {}
#         if role_name:
#             update['role_name'] = role_name
#         if description:
#             update['description'] = description
#         if list_order:
#             update['list_order'] = list_order
#         if status:
#             update['status'] = status
#
#         try:
#             cls.dbs.query(cls).filter(cls.role_id == role_id).update(update)
#             cls.dbs.commit()
#             return True
#         except:
#             cls.dbs.rollback()
#             raise
#
#     @classmethod
#     def get(cls, role_id):
#         item = cls.dbs.query(cls.role_id, cls.role_name, cls.description, cls.list_order,
#                                 cls.status).filter(cls.role_id == role_id).first()
#         return item and cls.initialize(item)
#
#     @classmethod
#     def gets(cls, start=0, limit=20, sort='id', order='asc'):
#         return cls.dbs.query(cls.role_id, cls.role_name, cls.description, cls.list_order,
#                                 cls.status).offset(start).limit(limit).all()
#
#     @classmethod
#     def get_count(cls):
#         return cls.dbs.query(cls).count()
#
#     @classmethod
#     def get_by_rolename(cls, role_name):
#         item = cls.dbs.query(cls).filter(cls.role_name == role_name).first()
#         return item and cls.initialize(item)