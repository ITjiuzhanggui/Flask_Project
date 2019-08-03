# 2.1 导入蓝图对象
from . import index_blue
from flask import render_template, current_app


# 2.2 使用蓝图对象实现路由
@index_blue.route('/')
def index():
    return render_template('news/index.html')


# 处理浏览器自动访问网站图标的路由
@index_blue.route('/favicon.ico')
def favicon_ico():
    # 使用current_app,发送静态文件(图片/文本/js/html)
    return current_app.send_static_file('news/favicon.ico')
