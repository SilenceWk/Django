# 社团管理系统说明

### 项目运行

1.下载 requirements.txt 文件中所需项目环境.

2.修改配置文件中的数据库连接设置.

3.执行数据迁移.

4.创建后台管理员账户.

5.完成测试.

```
coding:
1. pip install -r requirements.txt
2. 修改 LM 目录下的 settings.py 文件:
	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test2', # 数据库名
        'USER': 'root',	# 用户名
        'PASSWORD': '123456', # 密码
        'HOST': 'localhost', 
        'PORT': '3306',
    }
}
3. 生成迁移文件  python manage.py makemigrations
4. 执行迁移 python manage.py migrate
5. 开启服务 python manage.py runserver
```

 

### 功能实现

1. 用户的注册, 登录, 注销.

2. 社长可以管理社团成员, 执行本社团成员的移出.

3. 社长可以添加本社团信息, 可以为社团添加图片.

4. 社长可以创建社团活动.

5. 普通成员查看社团的信息,社团成员的信息,并加入社团.

6. 后台管理员 可以查看各个社团的具体信息.

7. 后台管理员可以查看每个用户.

8. 后台管理员可以进行权限设置, 委任社长等系列操作.

   ​

### 