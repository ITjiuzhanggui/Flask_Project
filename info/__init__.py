# 创建app及配置app相关的代码
import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config


# 提供一个函数，工厂方法，方便的根据不同的参数，实现不同的配置加载
def creat_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_name)

    # 插件数据库
    db = SQLAlchemy(app)

    # 创建redis对象
    redis_store = redis.StrictRedis(host=config_name.REDIS_HOST, port=config_name.REDIS_PORT)

    # 开启CSRF保护---> 会启用csrf_token对比机制
    CSRFProtect(app)

    # 设置Flask_Session扩展，将存在浏览器的cookie中的session数据，同步到服务器的指定地址中(redis)
    Session(app)

    return app
