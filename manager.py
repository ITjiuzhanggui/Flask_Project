# 管理程序启动
import redis
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import Config

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
