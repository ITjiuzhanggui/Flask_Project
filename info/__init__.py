# 创建app及配置app相关的代码
import redis
import logging
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler

# 创建数据库
db = SQLAlchemy()

# 定义一个空redis存储对象
redis_store = None


def setup_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config_name.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保护的路径，每个日志文件的最大大小，保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式，日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 提供一个函数，工厂方法，方便的根据不同的参数，实现不同的配置加载
def creat_app(config_name):
    # 配置项目日志
    setup_log(config_name)

    app = Flask(__name__)

    app.config.from_object(config_name)

    # 几乎所有的扩展都支持这种创建方式
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_name.REDIS_HOST, port=config_name.REDIS_PORT)

    # 开启CSRF保护---> 会启用csrf_token对比机制
    CSRFProtect(app)

    # 设置Flask_Session扩展，将存在浏览器的cookie中的session数据，同步到服务器的指定地址中(redis)
    Session(app)

    # 蓝图在用到的时候在导包，可以当作固定规则   
    from info.modules.index import index_blue
    # 注册(index)蓝图对象
    app.register_blueprint(index_blue)

    from info.modules.passport import passport_blue
    # 注册(passport)蓝图对象
    app.register_blueprint(passport_blue)

    return app


