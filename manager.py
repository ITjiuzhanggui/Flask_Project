from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    # 配置SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/Flask_Project'
    SQLALCHEMY_TRACK_MODIFICATIONS = Flask


app = Flask(__name__)

# 插件数据库
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
