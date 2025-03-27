from django.shortcuts import redirect
import time
from wlapp.models import VisitLog
import datetime
def login_check_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        login_user = request.session.get('user')
        print("login_user:",login_user)
        print("request.path:",request.path)

        white_list=['/login/','/captcha/']
        is_white = False
        for white_path in white_list:
            if white_path in request.path:
                is_white = True
        if login_user is None and is_white is False:
            return redirect("/login/")
        # 这里判断如果未登录，就定向至/login/
        # 下面的是对已经登陆的进行后续中间件处理

        admin_urls =["/users_manage/"]
        if login_user is not None:
            role = login_user.get("role")
            if role == "normal":
                for admin_url in admin_urls:
                    if admin_url in request.path:
                        return redirect("/show_excel/")

        
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def visit_log_middle(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = time.time()

        response = get_response(request)

        end_time = time.time()

        used_time = end_time - start_time
        username = ""
        if request.session.get("user"):
            username = request.session.get("user").get("username")
        ip = get_client_ip(request)
        curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = request.path

        VisitLog.objects.create(
            username=username,
            ip=ip,
            curr_time=curr_time,
            path=path,
            used_time=used_time
        )

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware