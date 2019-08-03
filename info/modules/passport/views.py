# 2.1 导入蓝图对象
from flask import request

from info import redis_store
from . import passport_blue
from info.utils.captcha.captcha import captcha


# 2.2 使用蓝图对象实现路由

# 获取图像验证码
# URL：/image_code
# 请求方式：GET
# 参数：image_code_id


@passport_blue.route('/image_code')
def get_image_code():
    # 1.获取参数
    image_code_id = request.args.get('image_code_id')
    # 2.生成验证码图像
    name, text, image_data = captcha.generate_captcha()
    # 3.保存redis
    redis_store.set('ImageCodeID_' + image_code_id, image_code_id, 300)
    # 4.返回图像
    return image_data
