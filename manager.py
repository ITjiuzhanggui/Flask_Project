# 管理程序启动
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import creat_app, db
from config import DevelopmentConfig, ProductionConfig

# 通过create_app,传递不同的配置信息，来实现manager以不同模式来启动
app = creat_app(DevelopmentConfig)

# 创建Manage
manager = Manager(app)

# 创建迁移对象
Migrate(app, db)

# 给Manager绑定迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)
    manager.run()
