# 2.1 导入蓝图对象
import random
import re

from flask import request, make_response, jsonify, current_app, session
from werkzeug.wrappers import json

from info import redis_store, db
from info.models import User
from info.utils.response_code import RET
from info.libs.yuntongxun.sms import CCP
from . import passport_blue
from info.utils.captcha.captcha import captcha
from info import constants


# 2.2 使用蓝图对象实现路由
# 注册用户
# 请求方式:POST
# URL:/register
# 参数:mobile,sms_code,password
@passport_blue.route('/register', methods=['POST'])
def register():
    """
    1.获取参数(3)
    2.校验参数(完整行，手机号)
    3.从redis中获取短信验证码
    4.对比验证码，对比失败返回信息
    5.对比成功，删除短信验证码
    6.对比成功注册用户(1.手机号是否注册过； 2.创建User对象；3.添加到mysql数据库)
    7.设置用户登陆--->session
    8.返回数据
    """
    # 一.获取数据
    # 1.获取参数(3)
    json_dict = request.json()
    mobile = json_dict.get('mobile')
    sms_code = json_dict.get('sms_code')
    password = json_dict.get('password')

    # 二.校验参数
    # 2.校验参数(完整性，手机号)
    if not all(mobile, sms_code, password):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    if not re.match('1[3456789][0-9]{9}', mobile):
        # 如果不匹配
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式不正确")

    # 三.逻辑处理
    # 3.从redis中获取短信验证码
    try:
        real_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库失败')
    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码过期或手机号填写错误')
    # 4.对比验证码，对比失败返回信息
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码填写错误')
    # 5.对比成功，删除短信验证码
    try:
        redis_store.delete('SMS_' + mobile)
    except Exception as e:
        current_app.logger.error(e)
        # 从用户体验来说，如果出错了，可以不用返回JSON信息
        # return jsonify(errno=RET.DBERR, errmsg='查询数据库失败')
    # 6.对比成功注册用户(1.手机号是否注册过 2.创建User对象 3.添加到mysql数据库)
    # 6.1 手机后是否注册过
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询mysql的用户信息失败')

    if user:
        # 说明用户已经注册
        return jsonify(errno=RET.DATAEXIST, errmsg='用户已经注册')

    # 6.2 创建User对象
    user = User()
    user.nick_name = mobile
    user.nick_name = mobile
    user.mobile = mobile
    # TODO 需要对密码做加密处理
    user.password_hash = password

    # 6.3添加到mysql数据库
    try:
        db.session.add()
        db.session.commit()
    except Exception as e:
        # 数据的修改操作，失败了需要回滚
        db.session.rollback()
        current_app.logger().error(e)
        return jsonify(errno=RET.DBERR, errmsg='添加mysql的用户信息失败')

    # 7.设置用户登陆 -> session
    session['user_id'] = user.id
    session['nickname'] = user.nick_name
    session['mobile'] = user.mobile

    # 四.返回数据
    return jsonify(errno=RET.OK, errmsg='注册成功')


# 获取短信验证码
# 请求方式post
# URL:/sms_code?mobile=130xxxxxxx&image_code=abcs&image_code_id=xxxx
# 参数：mobile,image_code,image_code_id
@passport_blue.route('/sms_code', methods=['POST'])
def get_sms_code():
    # 一，获取数据
    # 1.获取参数（手机号，图像验证码内容，图像验证码ID）
    # 局部数据更新需要使用JSON来传递数据
    # request.data返回的是字符串数据
    json_data = request.json
    mobile = json.data.get('mobile')
    image_code = json.data.get('image_code')
    image_code_id = json.data.get('image_code_id')

    # 二.校验数据
    # 2.检验数据(完整性，正则验证手机号)
    if not all([mobile, image_code, image_code_id]):
        # 如果参数不全，会进入该分支
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    if not re.match('1[3456789][0-9]{9}', mobile):
        # 如果不匹配
        return jsonify(errno=RET.DATAERR, errmsg='手机号格式不正确')

    # 三.逻辑处理
    # 3.从redis获取图像验证码models.py
    try:
        real_image_code = redis_store.get('ImageCodeTD_' + image_code_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis数据库查询失败')

    # 查询mysql&redis,都需要做判空处理
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='验证码已过期')

    # 4.将2个数据进行对比，对比失败，返回JSON数据
    if real_image_code.lower() != image_code.lower():
        # 对比失败，返回JSON数据
        return jsonify(errno=RET.DATAERR, errmsg="验证码填写错误")
    # 5.对比成功，生成短信验证码
    # '%06d':数字是6位的，不足以0补齐
    sms_code_str = '%06d' % random.ranint(0, 999999)

    # 6.保存到redis中
    try:
        redis_store.set("SMS_" + mobile, sms_code_str, constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        current_app.logger.error(e)
        # 保存短信验证码失败
        return jsonify(errno=RET.DATAERR, errmsg="保存短信验证码失败")

    # 7.调用云通讯发短信
    # result = CCP().send_template_sms(mobile, [sms_code_str, constants.SMS_TIME_DATE], 1)
    # if result != 0:
    #     # 发送失败
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送短信验证码失败")
    #
    # # 四.返回数据
    return jsonify(errno=RET.OK, errmsg="发送短信验证码成功")


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
        redis_store.set('ImageCodeID_' + image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
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
