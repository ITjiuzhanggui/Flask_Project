# 管理程序启动
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import app, db

# 创建Manage
manager = Manager(app)

# 创建迁移对象
Migrate(app, db)

# 给Manager绑定迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello_world():
    return 'hello world'


if __name__ == '__main__':
    manager.run()
