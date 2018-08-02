# -*- coding: utf-8 -*-


import tornado.web



class UiTopModule(tornado.web.UIModule):
    '''
    ui-top模块
    '''
    def render(self):
        return  self.render_string('modules/ui-top.html')

class LeftSideModule(tornado.web.UIModule):
    '''
    左侧边栏
    '''
    def render(self):
        return self.render_string('modules/left-side.html')


class TopHandlerModule(tornado.web.UIModule):
    '''
    顶部header
    '''
    def render(self):
        return self.render_string('modules/top-header.html')



class ShowDataTableModule(tornado.web.UIModule):
    '''
    展示数据 -- 表格

    '''
    def render(self,data, uri):
        return self.render_string('modules/show-data.html',
                                  data=data,
                                  uri=uri)

    def css_files(self):
        _css_file = [
            '/public/js/data-tables/DT_bootstrap.css',
            '/public/css/style.css',
            '/public/css/style-responsive.css',
        ]
        return _css_file

    def javascript_files(self):
        _js_file = [
            '/public/js/data-tables/jquery.dataTables.js',
            '/public/js/data-tables/DT_bootstrap.js',
            '/public/js/edit-data.js',
        ]
        return _js_file


    # def embedded_javascript(self):
    #     _js_str = '''
    #     jQuery(document).ready(function() {
    #     EditableTable.init();
    # });
    #     '''
    #     return _js_str



# #UIModule
uimodules = {
    'ui_top': UiTopModule,
    'left_side': LeftSideModule,
    'top_header': TopHandlerModule,
    'show_data': ShowDataTableModule,

}


#
__all__ = ['uimodules']