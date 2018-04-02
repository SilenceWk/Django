from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    url(r'^view_book/detail/$', views.detail, name='detail'),

    url(r'^join_club/(?P<uid>[0-9]+)$', views.join_club, name='join_club'),
    url(r'^user_show/(?P<id>[0-9]+)$', views.user_show, name='user_show'),
    url(r'^delete_user/(?P<userid>[0-9]+)$', views.delete_user, name='delete_user'),
    url(r'^change_club/(?P<id>[0-9]+)$', views.change_club, name='change_club'),

    url(r'^club_zixun_add$', views.club_zixun_add, name='club_zixun_add'),
    url(r'^club_zixun_insert$', views.club_zixun_insert, name='club_zixun_insert'),
    url(r'^show_act/$', views.show_act, name='show_act'),

    url(r'^show_act_detail/(?P<id>[0-9]+)$', views.show_act_detail, name='show_act_detail'),

    # 后台
    url(r'^myadmin/$', views.myadmin_index, name='myadmin_index'),
    url(r'^myadmin_reg/$', views.myadmin_reg, name='myadmin_reg'),
    url(r'^myadmin_usersinsert/$', views.myadmin_usersinsert, name='myadmin_usersinsert'),
    url(r'^myadmin_login/$', views.myadmin_login, name='myadmin_login'),
    url(r'^myadmin_dologin/$', views.myadmin_dologin, name='myadmin_dologin'),
    url(r'^myadmin_logout/$', views.myadmin_logout, name='myadmin_logout'),

    url(r'^myadmin_show_clubs/$', views.myadmin_show_clubs, name='myadmin_show_clubs'),
    url(r'^myadmin_club_info/(?P<id>[0-9]+)$', views.myadmin_club_info, name='myadmin_club_info'),
    url(r'show_members/(?P<id>[0-9]+)$', views.show_members, name='show_members'),
    url(r'del_member/(?P<id>[0-9]+)$', views.del_member, name='del_member'),

    # 更换社长
    url(r'^myadmin_change_member/(?P<id>[0-9]+)$', views.myadmin_change_member, name='myadmin_change_member'),
    url(r'^myadmin_weiren/(?P<id>[0-9]+)$', views.myadmin_weiren, name='myadmin_weiren'),
    url(r'^myadmin_show_all_members/$', views.myadmin_show_all_members, name='myadmin_show_all_members'),

    url(r'^myadmin_add_club/$', views.myadmin_add_club, name='myadmin_add_club'),

    url(r'^myadmin_insert_club/$', views.myadmin_insert_club, name='myadmin_insert_club'),

]
