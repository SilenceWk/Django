from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import re


class AdminMiddleware(object):

    def process_request(self, request):

        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin_login/', '/myadmin_dologin/', '/myadmin_logout/', '/myadmin_reg/', '/myadmin_usersinsert/']
        # 获取当前请求路径
        path = request.path
        # 判断当前请求是否是访问网站后台,并且path不在urllist中

        # 后台管理员用户adminuser
        if re.match("/myadmin", path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))


