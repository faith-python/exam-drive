# -*- coding: utf-8 -*-


redis = {
    # cookie_secret必须设置
    'cookie_secret': "2379874hsdhf0234990sdhsaiuofyasop977djdj",
    'xsrf_cookies': True,
    # 1 配置pycket 注意别忘记开启redis服务
    'pycket': {
        'engine': 'redis',
        'storage': {
            'host': '172.168.56.4',
            'port': 6379,
            'db_sessions': 10,
            'db_notifications': 11,
            'max_connections': 2 ** 31,
        },
        'cookies': {
            # 设置过期时间
            'expires_days': 2,
            #'expires':None, #秒
        },
    }
}


db = {
    'datebase': 'mysql',
    'connector': 'pymysql',
    'hostname': '172.168.56.4',
    'port': 3306,
    'user':'vfaith',
    'passwd': 'vfaith',
    'dbname': 'exam',
    'charset': 'utf8'

}



