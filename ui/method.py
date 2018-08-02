# -*- coding: utf-8 -*-


'''
定义自定义方法：
    该自定义方法可在模板调用，执行时需加（）；
        例如：自定义设置方法：
        def setting(self):
            pass
        自定义方法加入ui_methods字典：
            ui_methods={
                'setting': setting,
                }
        模板调用setting.html：
            {{ setting() }}

'''

from model.setting import Setting


def get_setting(self):
    '''
    获取系统设置信息
        title
        keyword
        etc...
    :param self:
    :return:
    '''
    return Setting.get_by_id(1)




def get_user_info(self):
    '''
    获取用户信息
    :param self:
    :return:
    '''
    if self.current_user:
        return db_model.UserModel.by_uuid(self.current_user)






ui_method={
    'setting':get_setting,
    'userinfo': get_user_info,
}





__all__ ={'ui_method'}