from django.shortcuts import render,redirect
from django.http import HttpResponse
from wangleiproject.settings import BASE_DIR
import pandas as pd
import string
import openpyxl
import random
from datetime import datetime
from wlapp.models import User
from django.core.paginator import Paginator
from wlapp.forms import UserForm
from wlapp.forms import UserModelForm
from wlapp.forms import LoginForm
# 记得加wlapp
from django.forms import model_to_dict
# 用的比较多，写函数在这里
# Create your views here.
def hello(request):
    # request 必须写
    return HttpResponse('hello django')
    # 返回字符串内容要HttpResponse（）封装

def show_excel(request):
    keyword=""
    if request.method=="POST":
        keyword=request.POST['keyword']
        keyword=str(keyword).strip()


    df=pd.read_excel(BASE_DIR/'data/数据-学生成绩表.xlsx')

    if keyword:
        df=df[(df['姓名']==keyword )| (df["学号"]==keyword)]
    # cont="""

    #     <table>
    #         <tr>
    #         <th>学号</th>
    #         <th>姓名</th>
    #         <th>语文</th>
    #         <th>数学</th>
    #         <th>英语</th>
    #     </tr>
    # """
    # for idx,row in df.iterrows():
    #     cont+="""
    #     <tr>
    #         <th>{row.学号}</th>
    #         <th>{row.姓名}</th>
    #         <th>{row.语文}</th>
    #         <th>{row.数学}</th>
    #         <th>{row.英语}</th>
    #     </tr>
    #     """
    # cont+="""
    #     </table>
    # """
    # return HttpResponse(cont)
    return render(request,'show_excel3.html',{'df':df,"keyword":keyword})
    # render(request,'show_excel')第一个为参数，第二个为路径默认从当前wlapp下的templates下找


def testjs(request):
     return render(request,'testjs.html',{})

def getnewpwd(request):
    words=list(
        string.ascii_lowercase
        +string.ascii_uppercase
        +string.digits
        +string.punctuation
    )
    random.shuffle(words)

    result="".join(words[:20])
    return HttpResponse(result)

def users_manage(request):
    #users = User.objects.all()
    users = User.objects.order_by("-create_time")[:5]#创建时间倒序排列
    if request.method=="POST":
        keyword=request.POST.get("keyword") 
        if keyword is not None and keyword!="":
            users = User.objects.filter(username=keyword).order_by("-create_time")


    return render(request,"users_manage.html",{"users":users})


# manage1的变种，前后端代码进行了调整
def users_manage1(request):
    #users = User.objects.all()
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
    # 上面三行可用中间件代替
    users = User.objects.order_by("-create_time")#创建时间倒序排列
    if request.method=="POST":
        keyword=request.POST.get("keyword") 
        if keyword is not None and keyword!="":
            users = User.objects.filter(username=keyword).order_by("-create_time")


    users_pages=Paginator(users,10)
    page_number=int(request.GET.get("page",1))
    if page_number > users_pages.num_pages:
        page_number=1
    # 前端如果返回page，就用page参数，否则是1
    users_page= users_pages.page(page_number)


    return render(request,"users_manage.html",{"users_page":users_page})
# 注意前后端参数名的一致

def django_syntax(request):
    datadict={
        "username":"bigwang",
        "grades":{"语文":88,"数学":99,"英语":78,},
        "likes":["篮球","足球","排球",],
        "welcome":"welcome to django study",
        "now":datetime.now(),
        "role":"vip",
        "students":[{"id":101,"name":"xiaoming"},
                    {"id":102,"name":"xiaowang"},
                    {"id":103,"name":"xiaozhao"},]


    }

    return render(request,"django_syntax.html",datadict)

def user_add(request):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    err_msg=""
    if request.method=="POST":
        username = request.POST.get('username')
        if not username:
            err_msg+="用户名不能为空"

        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not password or not password_confirm or password_confirm!=password or len(password)<6:

            err_msg+="密码需要两次相等并且大于6位"

        gender = request.POST.get('gender')
        if not gender or not str(gender).isnumeric():
            err_msg+="请选择性别" 

        role = request.POST.get('role')
        if not role:
            err_msg+="请选择角色"

        age = request.POST.get('age')

        if not age or not str(age).isnumeric():
            err_msg+="请输入年龄"
        db_user = User.objects.filter(username=username)

        if len(db_user)>0:
            err_msg+="用户名在数据库已经存在了；"
        if err_msg == "":
            User.objects.create(
                username=username,
                password=password,
                gender=gender,
                age=age,
                role=role,
                create_time=datetime.now()
            )
            return redirect("/users_manage/")
        
    return render(request,"user_add.html",{"err_msg":err_msg})

def user_add1(request):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    err_msg=""
    if request.method == "POST":
        err_msg = check_addupdate_user(request.POST)
        db_user=User.objects.filter(username=request.POST.get('username'))

        if len(db_user)>0:
            err_msg += "用户名在数据库已经存在了；"
        
        if err_msg == "":
            User.objects.create(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                role=request.POST.get('role'),
                create_time=datetime.now()
            )
            
            return redirect("/users_manage/")
        
    return render(request,"user_add.html",{"err_msg":err_msg})


# formd方法的代码
def user_add_form(request):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    if request.method=="GET":
        form = UserForm()
    else:
        form = UserForm(request.POST)
        form.set_update(False)
        # 把request.POST的方法提供给UserForm这个类，该类本身可以提供校验方法
        #UserForm 类继承自 forms.Form，在创建表单实例时，
        #Django 会自动根据字段的定义对 request.POST 中的数据进行基本的字段级别校验。


    # 存数据
        if form.is_valid():
            User.objects.create(
                username = form.cleaned_data.get("username"),
                password = form.cleaned_data.get("password"),
                gender = form.cleaned_data.get("gender"),
                role = form.cleaned_data.get("role"),
                create_time=datetime.now(),
                )
            return redirect("/users_manage/")
    return render(request,"user_add_form.html",{"form":form})

def user_add_model(request):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    if request.method=="GET":
        form = UserModelForm()
    else:
        user=User(create_time=datetime.now())
        # 为model创建create_time参数
        form = UserModelForm(request.POST,request.FILES,instance=user)
        # 有文件要加request.FIELs
        form.set_update(False)
        # 把request.POST的方法提供给UserForm这个类，该类本身可以提供校验方法
        #UserForm 类继承自 forms.Form，在创建表单实例时，
        #Django 会自动根据字段的定义对 request.POST 中的数据进行基本的字段级别校验。


    # 存数据
        if form.is_valid():
            form.save()
            return redirect("/users_manage/")
    return render(request,"user_add_model.html",{"form":form})





def user_delete(request,user_id):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    # 删除
    User.objects.filter(id=user_id).delete()
    # filter：返回0个或者更多个queryset，无论查询结果是否有匹配记录，都不会报错。没有匹配记录时，返回一个空的 QuerySet 。
    # get：要求查询结果必须有且仅有一条记录。如果没有找到匹配的记录，会抛出 DoesNotExist 异常；如果找到多条记录，会抛出 MultipleObjectsReturned 异常。

    return redirect("/users_manage/")

def user_edit(request, user_id):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
    # 修改
    db_user=User.objects.get(pk=user_id)
    err_msg = ""
    if request.method =="POST":
        err_msg = check_addupdate_user(request.POST)
        db_user.gender = request.POST.get("gender")
        db_user.age = request.POST.get("age")
        db_user.password = request.POST.get("password")
        db_user.role = request.POST.get("role")
        if err_msg == "":
            db_user.save()
            return redirect("/users_manage/")
    return render(request,"user_edit.html",{"user":db_user,"err_msg":err_msg})


def user_edit_form(request,user_id):  
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/') 
        # 上面三行可用中间件代替
    # db_user=User.objects.get(id=user_id)
    db_user=User.objects.get(pk=user_id)
    if request.method == "GET":
        form=UserForm(initial=model_to_dict(db_user))
    else:
        # 这儿指的是post方法
        form = UserForm(request.POST)
        # 问题是会丢进去之后会进行校验 使用clean，和clean_username方法
        form.set_update(True)
        if form.is_valid():
            db_user.username = form.cleaned_data.get("username")
            db_user.password = form.cleaned_data.get("password")
            db_user.gender = form.cleaned_data.get("gender")
            db_user.role = form.cleaned_data.get("role")
            db_user.create_time=datetime.now()
            db_user.save()
            return redirect("/users_manage/")
    form.fields['username'].widget.attrs["readonly"] = True
    return render(request,"user_edit_form.html",{"form":form})

def user_edit_model(request,user_id):
    login_user = request.session.get("user")
    if login_user is None:
        return redirect('/login/')
        # 上面三行可用中间件代替
    db_user=User.objects.get(pk=user_id)
    if request.method == "GET":
        form=UserModelForm(instance=db_user)
        # 注意instance用在model，initial用在from
    else:
        # 这儿指的是post方法
        form = UserModelForm(request.POST,request.FILES,instance=db_user)
        # 问题是会丢进去之后会进行校验 使用clean，和clean_username方法
        form.set_update(True)
        if form.is_valid():
            form.save()
            # form含有instance的数据，不许压迫bd_user.save()
            return redirect("/users_manage/")
        
    form.fields['username'].widget.attrs["readonly"] = True
    return render(request,"user_edit_model.html",{"form":form})


def check_addupdate_user(post_datas):

    err_msg=""
    username = post_datas.get('username')
    if not username:
        err_msg+="用户名不能为空"    
    password = post_datas.get('password')
    password_confirm = post_datas.get('password_confirm')
    if not password or not password_confirm or password_confirm!=password or len(password)<6:

        err_msg+="密码需要两次相等并且大于6位"
    gender = post_datas.get('gender')
    if not gender or not str(gender).isnumeric():
        err_msg+="请选择性别" 
    role = post_datas.get('role')
    if not role:
        err_msg+="请选择角色"
    age = post_datas.get('age')
    if not age or not str(age).isnumeric():
        err_msg+="请输入年龄"
    
    return err_msg


def login(request):
    if request.method =="GET":
        form=LoginForm()
    else:
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            db_user=User.objects.filter(
                username=username,
                password=password
            ).first()
            if db_user is None:
                form.add_error("password","用户名称或者密码不对")
            else:
                request.session['user']={"id":db_user.id,"username":db_user.username,"role":db_user.role}
                return redirect("/users_manage/")
    return render(request,"login.html",{"form":form})

def logout(request):
    request.session.clear()
    return redirect("/login/")


