# 2.1 导入蓝图对象
from . import index_blue


# 2.2 使用蓝图对象实现路由
@index_blue.route('/')
def hello_world():
    # logging.debug("this is debug")
    # logging.info("this is debug")
    # logging.warning("this is debug")
    # logging.error("this is debug")
    # logging.fatal("this is debug")
    return 'hello world'
