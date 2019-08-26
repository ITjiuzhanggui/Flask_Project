# 管理程序配置信息
import redis
import logging


class Config(object):
    # 配置SQLAlchemy
    "密码：password"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@127.0.0.1/Flask_Project'
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


class DevelopmentConfig(Config):
    """开发模式下的配置"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING
