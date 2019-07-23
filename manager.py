# 管理程序启动
import redis
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    # 配置SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/Flaks_Project'
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SECRET_KEY = 'k6hNvTTViU907RiQ8IbI5lgRrgGSvaUF81a58jiiet/6NqTG5kqi/Iin/HTiZdRXNnmLqzY5Ejt6UYfeJWqsdA=='

    # 配置flask-session扩展
    SESSION_TYPE = 'redis'  # 设置要同步的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 开启签名
    PERMANENT_SESSION_LIFETIME = 86400 * 7  # 设置过期时间

    DEBUG = True


app = Flask(__name__)

app.config.from_object(Config)

# 插件数据库
db = SQLAlchemy(app)

# 创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 开启CSRF保护---> 会启用csrf_token对比机制
CSRFProtect(app)

# 设置Flask_Session扩展，将存在浏览器的cookie中的session数据，同步到服务器的指定地址中(redis)
Session(app)

# 创建Manage
manager = Manager(app)

# 创建迁移对象
Migrate(app, db)

# 给Manager绑定迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    session['name'] = 'intel'
    return 'hello world'


if __name__ == '__main__':
    manager.run()
