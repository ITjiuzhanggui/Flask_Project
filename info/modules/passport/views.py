# 2.1 导入蓝图对象
from . import passport_blue


# 2.2 使用蓝图对象实现路由
@passport_blue.route('/')
def passport_blue():
    return 'abc'
