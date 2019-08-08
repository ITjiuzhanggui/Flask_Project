# 2.1 导入蓝图对象
from flask import request, make_response, jsonify, current_app

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

    try:
        # 可以给redis增加类型注释来查看
        redis_store.set('ImageCodeID_' + image_code_id, text, 300)
    except Exception as e:
        # 保存日志
        current_app.logger.error(e)
        # 返回json格式
        # 如果要全局更新网页，可以渲染模版；
        # 如果只是局部更新数据，前后端只需要使用json传输即可
        # "{'errno':4001, 'errmsg': '保存redis出错'}"
        return jsonify(errno=4001, errmsg='保存redis出错')

    # 4.返回图像
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response
