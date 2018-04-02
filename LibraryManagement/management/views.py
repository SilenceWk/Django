from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Club, Img, club_zixun, Myadmin
from django.core.urlresolvers import reverse
from management.utils import permission_check
import time,PIL,os
from PIL import Image

def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Club(
                name=request.POST.get('name', ''),
                detail=request.POST.get('detail', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'management/add_book.html', content)


def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    # category_list = Club.objects.values_list('category', flat=True).distinct()
    # print(category_list)
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Club.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Club.objects.all()
        i = []
        for club in book_list:
            if club.category not in i:
                # print(club.category)
                i.append(club.category)
        category_list = i
    else:
        book_list = Club.objects.filter(category=query_category)
        i = []
        for club in book_list:
            if club.category not in i:
                # print(club.category)
                i.append(club.category)
        category_list = i

        # print(club.category)
        # book_list = Club.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Club.objects.filter(name__contains=keyword)
        print(book_list)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    # print(category_list)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    return render(request, 'management/view_book_list.html', content)


def detail(request):
    user = request.user if request.user.is_authenticated() else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Club.objects.get(pk=book_id)
        need_user = MyUser.objects.get(user_id=user.id)
        content = {
            'user': need_user,
            'active_menu': 'view_book',
            'book': book,
        }
    except :
        return redirect(reverse('login'))
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    book=Club.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Club.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Club.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)


def user_show(request, id):
    users = MyUser.objects.filter(uid=id)
    context = {'users': users}
    return render(request, 'management/user_show.html', context)

def join_club(request, uid):
    id = request.user.id
    # print(id)
    user = MyUser.objects.get(user_id=id)
    user.uid = uid
    user.save()
    return render(request, 'management/return.html')

def delete_user(request, userid):
    user = MyUser.objects.get(id=userid)
    user.uid = 0
    user.save()
    return render(request, 'management/delete_user.html')

def change_club(request, id):
    users = MyUser.objects.filter(uid=id)
    context = {'users': users}
    return render(request, 'management/change_club.html', context)

def club_zixun_add(request):
    return render(request, 'management/club_zixun_add.html')

def club_zixun_insert(request):
    try:
        # 判断并执行图片上传，缩放等处理
        myfile = request.FILES.get("pic", None)
        if not myfile:
            return HttpResponse("没有上传文件信息！")
        # 以时间戳命名一个新图片名称
        filename = str(time.time()) + "." + myfile.name.split('.').pop()
        path = os.path.join('./management/static/zixun/', filename)
        print(os.path.abspath(path))
        destination = open(path, 'wb+')
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # 执行图片缩放
        im = Image.open("./management/static/zixun/" + filename)
        im.thumbnail((400, 400))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./management/static/zixun/_s" + filename, 'jpeg')
        # 缩放到220*220:
        im.thumbnail((220, 220))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./management/static/zixun/_m" + filename, 'jpeg')


        ob = club_zixun()
        ob.activity_name = request.POST['activity_name']
        ob.activity_describe = request.POST['activity_describe']
        ob.activity_img = filename
        ob.activity_person = request.POST['activity_person']
        ob.save()
        context = {'info': '添加成功'}
        return render(request, 'management/myadmin/info.html', context)
    except Exception as e:
        print(e)
        context = {'info': '添加失败'}
        return render(request, 'management/myadmin/info.html', context)

def show_act(request):
    clubs = club_zixun.objects.all()
    context = {'clubs': clubs}
    return render(request, 'management/show_act.html', context)

def show_act_detail(request, id):
    club = club_zixun.objects.get(id= id)
    context = {'club': club}
    return render(request, 'management/show_act_detail.html', context)


# 后台
def myadmin_index(request):
    return render(request, 'management/myadmin/myadmin_show.html')

def myadmin_reg(request):
    return render(request, 'management/myadmin/useradd_2.html')

def myadmin_usersinsert(request):
    try:
        if request.POST['username'] and request.POST['password'] and request.POST['name'] and request.POST['email']:
            ob = Myadmin()
            ob.username = request.POST.get('username')
            ob.password = request.POST.get('password')
            ob.name = request.POST['name']
            ob.email = request.POST['email']
            ob.save()
            context = {'info': '注册成功'}
            return render(request, 'management/myadmin/info.html', context)
    except Exception as e:
        context = {'info': '注册失败'}
        return render(request, 'management/myadmin/info.html', context)
    context = {'info': '注册失败'}
    return render(request, 'management/myadmin/info.html', context)

# 登录
def myadmin_login(request):
    return render(request, 'management/myadmin/myadmin_login.html')

# 执行登录
def myadmin_dologin(request):
    try:
        # 获取数据库中对应的用户
        user = Myadmin.objects.get(username=request.POST['username'])
        # 判断密码是否相同
        if user.password == request.POST['password']:
            # 将用户信息存入 session
            request.session['adminuser'] = user.name
            return redirect(reverse('myadmin_index'))
        else:
            context = {'info': '登录失败, 请输入正确的密码'}
            return render(request, 'management/myadmin/info.html', context)
    except:
        context = {'info': '登录失败, 您输入的账号不存在'}
        return render(request, 'management/myadmin/info.html', context)


def myadmin_logout(request):
    del request.session['adminuser']
    return redirect(reverse('homepage'))

def myadmin_show_clubs(request):
    clubs = Club.objects.all()
    context = {'clubs': clubs}
    return render(request, 'management/myadmin/show_clubs.html', context)

def myadmin_club_info(request, id):
    club = Club.objects.get(id=id)
    context = {'club': club}
    return render(request, 'management/myadmin/show_club_info.html', context)

def show_members(request, id):
    users = MyUser.objects.filter(uid=id)
    context = {'users': users}
    return render(request, 'management/myadmin/show_members.html', context)

def del_member(request, id):
    user = MyUser.objects.get(id=id)
    user.uid = 0
    user.save()
    context = {'info': '移除本社成功'}
    return render(request, 'management/myadmin/myadmin_info.html', context)

def myadmin_change_member(request, id):
    users = MyUser.objects.filter(uid=id)
    context = {'users': users}
    return render(request, 'management/myadmin/myadmin_change_member.html', context)

def myadmin_weiren(request, id):
    old_shezhang = MyUser.objects.get(permission=2)
    old_shezhang.permission = 1
    new_shezhang = MyUser.objects.get(id=id)
    new_shezhang.permission = 2
    # print(new_shezhang, new_shezhang.permission)
    uid = new_shezhang.uid
    club = Club.objects.get(id=uid)
    club.author = new_shezhang.nickname
    old_shezhang.save()
    new_shezhang.save()
    club.save()
    context = {'info': '委任成功'}
    return render(request, 'management/myadmin/myadmin_info.html', context)

def myadmin_show_all_members(request):
    users = MyUser.objects.all()
    context = {'users': users}
    return render(request, 'management/myadmin/myadmin_show_all_members.html', context)


def myadmin_add_club(request):
    return render(request, 'management/myadmin/myadmin_add_club.html')

def myadmin_insert_club(request):
    try:
        ob = Club()
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.author = request.POST['author']
        ob.publish_date = request.POST['publish_date']
        ob.category = request.POST['category']
        ob.detail = request.POST['detail']
        ob.save()
        context = {'info': '添加社团成功'}
        return render(request, 'management/myadmin/myadmin_info.html', context)
    except Exception as e:
        print(e)
        context = {'info': '添加社团失败'}
        return render(request, 'management/myadmin/myadmin_info.html', context)
