# -*- coding: utf-8 -*-

# @Author: Faith <faith_python@foxmail.com>
# @Date: 18-3-19

__author__ = 'Faith'



from random import randint, choice
from PIL import Image, ImageDraw, ImageFont
from string import printable


from io import BytesIO




class Captcha():


    #生成随机验证码
    @property
    def _rand_text(self):
        # 生成验证码
        text = ''.join([choice(printable[:62]) for i in range(4)])
        return text


    #创建图像
    def _create_img_buffer(self):
        '''\
        创建验证码
        :return: 验证码 验证码图片的 byte数据流
        '''
        font_path = "util/verify/font/Arial.ttf"

        font_color = (randint(150, 200), randint(0, 150), randint(0, 150))

        line_color = (randint(0, 150), randint(0, 150), randint(150, 200))

        point_color = (randint(0, 150), randint(50, 150), randint(150, 200))

        width, height = 100, 40
        image = Image.new('RGB', (width, height), (200, 200, 200))


        font = ImageFont.truetype(font_path, height - 10)
        draw = ImageDraw.Draw(image)
        captcha_text = self._rand_text
        font_width, font_height = font.getsize(captcha_text)

        # 把验证码写到画布上
        draw.text((10, 10), captcha_text, font=font, fill=font_color)

        # 绘制线条
        for i in range(0, 5):
            draw.line(((randint(0, width), randint(0, height)),
                       (randint(0, width), randint(0, height))),
                      fill=line_color, width=2)

        # 绘制点
        for i in range(randint(100, 1000)):
            draw.point((randint(0, width), randint(0, height)), fill=point_color)

        img_buffer = BytesIO()
        image.save(img_buffer, format='jpeg')
        content = img_buffer.getvalue() #图片 byte流

        return captcha_text, content

    #获取验证码, 验证码图片 byte数据流
    @property
    def get_text_buffer(self):
        '''
        获取验证码信息
        :return: 验证码 验证码图片的 byte数据流
        '''
        return self._create_img_buffer()




if __name__ == '__main__':

    test = Captcha()

    test.get_captcha