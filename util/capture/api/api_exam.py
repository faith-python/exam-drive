# -*- coding: utf-8 -*-


import json
import requests


_JUHE_KEY = '015b1f246bfcf9a5db3999361bfa0396' # 聚合 API key

_JUHE_API_URL = 'http://v.juhe.cn/jztk/' # api url


def exam(subject,
         model,
         testType='rand',
         _appkey=_JUHE_KEY):
    '''
    key	string	是	您申请的appKey
 	subject	int	是	选择考试科目类型，1：科目1；4：科目4
 	model	string	是	驾照类型，可选择参数为：c1,c2,a1,a2,b1,b2；当subject=4时可省略
 	testType	string	否	测试类型，rand：随机测试（随机100个题目），order：顺序测试（所选科目全部题目）
    :return:
        {
                 "reason":"ok",
                 "error_code":0,
                [
                    {'url': 'http://images.juheapi.com/jztk/c1c2subject1/7.jpg',
                        'question': '这个标志是何含义？',
                        'explains': '注意危险：用以促使车辆驾驶员谨慎慢行。',
                         'item2': '注意危险',
                         'id': '7',
                         'item4': '事故多发路段',
                         'item3': '拥堵路段',
                         'item1': '减速慢行',
                         'answer': '2'
                    },
                ],...
                }
    '''

    information_url = _JUHE_API_URL + 'query'

    payload = {
        'subject': subject,     # 选择考试科目类型，1：科目1；4：科目4
        'model': model,         # 驾照类型，可选择参数为：c1,c2,a1,a2,b1,b2；当subject=4时可省略
        'testType': testType,   # 测试类型，rand：随机测试（随机100个题目），order：顺序测试（所选科目全部题目）
        'key': _appkey,          # 您申请的appKey
    }

    headers = {
        'Host': 'v.juhe.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36',
    }

    try:
        response = requests.post(information_url,
                                 data=payload,
                                 headers=headers)

        json_content = response.json() # 读取json返回内容
        # print(type(json_content)) ### 类型为dict

        #解析内容
        error_code = json_content.get('error_code') # 读取状态

        if error_code == 0:
            result_data = json_content.get('result') # [:15]
            # print(type(result_data)) ### 类型为list

            ''' 返回内容:
               {
                    "reason":"ok",
                    "error_code":0,
                   [
                       {'url': 'http://images.juheapi.com/jztk/c1c2subject1/7.jpg', 
                           'question': '这个标志是何含义？', 
                           'explains': '注意危险：用以促使车辆驾驶员谨慎慢行。',
                            'item2': '注意危险', 
                            'id': '7', 
                            'item4': '事故多发路段', 
                            'item3': '拥堵路段', 
                            'item1': '减速慢行', 
                            'answer': '2'
                       }, 
                   ],...
                   }
            '''
            # print(len(result_data))
            # print(result_data)
            totaltask = len(result_data)


        else:
            result_data = json_content
            '''
            {
                "reason": "\u9519\u8bef\u7684\u8bf7\u6c42KEY!", 
                "error_code": 10001, 
                "result": null, 
                "resultcode": "101"
            }
            '''
        # print(result_data)
        return json.dumps(result_data)

    except Exception:
        pass








if __name__ == '__main__':
   data =exam(1, 'c1', 'rand')
   print(data)