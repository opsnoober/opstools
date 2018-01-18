#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader("app","templates"))

result = [
	("ip","username","passwd","Ubuntu 16.04.3","4","8","50","私有云","项目测试环境","xx","项目","2018-3-18"),
]

template = env.get_template("a.html")

html = template.render(result=result)
