# -*- coding: utf-8 -*-



import requests
import uuid

'''
API接口对接
AppID
（应用ID）
	
a99920f227204d70854add761b9dc138
	
复制
Account Sid
（用户sid）
	
3c4ce8a02fce99fb857cf251ddc996bb
	
复制
Auth Token
（鉴权密钥）
	
74ae015d2ffd59a4a945e6878a90d76b
Rest URL
（请求地址）
	
https://open.ucpaas.com/ol/sms/{function}
	https://open.ucpaas.com/ol/sms/sendsms	
复制
'''
class Sendsms(object):
    '''\
        发送验证码
    '''
    def __init__(self, mobile, param, templateid='294941'):
        '''
        :param mobile: 用户手机号
        :param param: 验证码内容--->模板中的替换参数，
                        如该模板不存在参数则无需传该参数或者参数为空，
                        如果有多个参数则需要写在同一个字符串中，
                        以英文逗号分隔 （如：“a,b,c”），
                        参数中不能含有特殊符号“【】”和“,”
        :param templateid: 云之讯模板id
        '''
        self.url = 'https://open.ucpaas.com/ol/sms/sendsms'
        self.sid = '3c4ce8a02fce99fb857cf251ddc996bb'
        self.token = '74ae015d2ffd59a4a945e6878a90d76b'
        self.appid = 'a99920f227204d70854add761b9dc138'
        self.templateid = templateid
        self.param = param
        self.moblie = mobile
        self.uid = uuid.uuid4().hex

    @property
    def _payload(self):
        '''
        组装待发送参数
        :return:
        '''
        data = {
            'sid': self.sid,
            'token': self.token,
            'appid': self.appid,
            'templateid': self.templateid,
            'param': self.param,
            'mobile': self.moblie,
            'uid': self.uid,
        }
        return data

    @property
    def send_sms(self):
        '''
        发送验证码短信
        :return:
        '''
        try:
            response = requests.post(url=self.url,
                                     json=self._payload,
                                     )

        except requests.exceptions.HTTPError as e:
            print('发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应). result:', e)
        except requests.exceptions.ConnectionError as e:
            print('请检查你的网络! result:', e)
        except requests.exceptions.RequestException as e:
            print('request错误! result:', e)
        else:
            if response.status_code == 200:
                data = response.json()
                # print(data)
                code = data['code']
                msg = data['msg']
                if code == '000000' and msg== 'OK':
                    return True
                else:
                    return False
        return False




if __name__ == '__main__':
    test = Sendsms(15885789044,'123412')
    print(test.send_sms)