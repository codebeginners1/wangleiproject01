from django.contrib import admin
from django.urls import path,include
from wlapp import views
from wlapp import views_order
from wlapp import views_agg

# 记得加wlapp
urlpatterns = [
    path('hello/', views.hello),
    # shift + alt+下 复制
    path('show_excel/', views.show_excel),
    path('testjs/', views.testjs),
    path('getnewpwd/',views.getnewpwd),
    path('users_manage/',views.users_manage1),
    path('',views.users_manage1),
    path('user_add/',views.user_add1),
    path('user_add_form/',views.user_add_form),
    path('user_add_model/',views.user_add_model),
    
    path('user_delete/<int:user_id>',views.user_delete),# 这个ur里面可以带参数，int声明类型
    path('user_edit/<int:user_id>',views.user_edit),# 这个ur里面可以带参数，int声明类型
    path('user_edit_form/<int:user_id>',views.user_edit_form),# 这个ur里面可以带参数，int声明类型
    path('user_edit_model/<int:user_id>',views.user_edit_model),# 这个ur里面可以带参数，int声明类型
    path('login/',views.login),
    path('logout/',views.logout),

    path('django_syntax/',views.django_syntax),
    path('captcha/', include('captcha.urls')),
    path('order_manage/',views_order.order_manage1),
    path('order_manage/',views_order.order_manage1),
    path('tianqi_agg/',views_agg.tianqi_manage),
    path('get_year_table/',views_agg.get_year_table),
    path('get_tianqi_line/',views_agg.get_tianqi_line),
    path('get_tianqi_bar/',views_agg.get_tianqi_bar),
    path('get_tianqi_pie/',views_agg.get_tianqi_pie),
]