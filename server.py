# -*- coding: utf-8 -*-

import os.path

import tornado.httpserver
import tornado.web
import tornado.ioloop
import argparse
import sys


#本程序说明
argument_parser = argparse.ArgumentParser(#prog='exam-system',
                                          description='在线模拟考试系统!')

#设置参数
argument_parser.add_argument('-db', nargs=1, default=False, type=bool, help='初始化数据库,并加载数据!')



from tornado.options import options, define
# 设置启动端口
define("port", default=7000, type=int, help="运行在哪个端口")


from conf import config
from mainurls import urls_pattern as url_handlers
from ui import uimodules


applicaton = tornado.web.Application(
    handlers=url_handlers,
    template_path='template',
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    login_url='/login',
    debug=True,
    **config.redis,
    # ui_methods=ui_method,
    ui_modules=uimodules,

)






def capture_data():
    # 抓取数据
    #获取数据至数据库
    from util.capture.savedata import SaveQuestionData
    from util import db
    from model.user import UserModel
    from model import carquestion
    def _initialize_db():
        '''
        创件数据表
        :return:
        '''
        print('初始化数据库')
        try:
            db.create_all()
        except Exception as e:
            print('Error:{}'.format(e))
        else:
            print('初始化数据库表完成!')


    def _init_admin():
        admin_info = '初始化管理员失败!!!'
        admin_user = UserModel.new(
            username='11111111111',
            password='123456a',
            nickname='超级管理员',

        )
        db.datebase_session.add(admin_user)
        try:
            db.datebase_session.commit()
        except Exception as e:
            print(e)
            db.datebase_session.rollback()
        else:
            print('管理员初始化成功!')
            admin_info = '''
            管理员用户名: 11111111111
            管理员密码: 123456a
            '''
        finally:
            db.datebase_session.close()

        return admin_info



    try:
        _initialize_db()
        print('正在请求数据!!!!')
        SaveQuestionData('small').save_to_database()
        SaveQuestionData('truck').save_to_database()
        SaveQuestionData('bus').save_to_database()
        SaveQuestionData('4').save_to_database()  # 科目4题库
        print('保存完成!')
        if not UserModel.get_all():
            is_success_admin = _init_admin()
            print(is_success_admin)
    except Exception as e:
        print('请检查你的网络!!!!')
        sys.exit(0)



def main():
    arguments = argument_parser.parse_args()
    if arguments.db:
        capture_data()
    # tornado.options.parse_command_line()
    httpserver = tornado.httpserver.HTTPServer(applicaton)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print('系统启动 ....')
    main()
