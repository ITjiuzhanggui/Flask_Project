# 管理程序配置信息
import redis


class Config(object):
    # 配置SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/Flaks_Project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

