# 编写数据库的表的模式
from django.db import models





# Create your models here.

"""
id:自增id，用户id
username：用户名，最多字符串120个字符
password：密码，最多60个字符

gender：性别，数字0和数字1，只能是男，女两个选项

role：角色，字符串最多20个字符，admin是管理员，normal是普通用户

create_time:创建时间，datetime形式

///


"""
class User(models.Model):
    username=models.CharField(verbose_name="用户名",max_length=120)
    password=models.CharField(verbose_name="密码",max_length=60) 
    choices=[(1,"男"),(0,"女")]
    age=models.IntegerField(verbose_name="年龄",default=18)
    gender=models.IntegerField(verbose_name="性别",choices=choices)
    role_choices =[('admin',"管理员"),("normal","普通用户")]
    role=models.CharField(verbose_name="角色",choices=role_choices,max_length=20,default="normal")
    create_time=models.DateField(verbose_name="创建时间")

    head_img=models.ImageField(verbose_name="头像",upload_to="head_img",default="")
    # 上传到media的head_img文件夹下，default是默认头像，也可以用Field



class VisitLog(models.Model):
    """
        used_time = end_time - start_time
        username = ""
        if request.session.get("user"):
            username = request.session.get("user").get("username")
        ip = get_client_ip(request)
        curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = request.path
    """
    ip = models.CharField(verbose_name="访问IP", max_length=30)
    username = models.CharField(verbose_name="用户名", max_length=128)
    curr_time = models.CharField(verbose_name="当前时间", max_length=20)
    path = models.CharField(verbose_name="访问路径", max_length=128)
    used_time = models.FloatField(verbose_name="访问耗时")


class OrderData(models.Model):
    """ '单号', '产品名称', '成本价', 
    '销售价', '销售数量', '产品成本',
    '销售收入', '销售利润'
    """

    order_id = models.IntegerField(verbose_name="订单号",primary_key=True)
    product_name = models.CharField(verbose_name="产品名称", max_length=128)
    cost_price = models.IntegerField(verbose_name="成本价")
    sale_price = models.IntegerField(verbose_name="销售价")
    sale_num = models.IntegerField(verbose_name="销售数量")
    product_cost = models.IntegerField(verbose_name="产品成本")
    sale_income = models.IntegerField(verbose_name="销售收入")
    sale_profit = models.IntegerField(verbose_name="销售利润")
    def __str__(self):
        return f"{self.order_id} - {self.product_name}"


class TianQiData(models.Model):
    """
    '日期', '最高温度', '最低温度', '天气', '风力风向', '星期'
    """
    date = models.DateField(verbose_name="日期")
    max_temperature = models.IntegerField(verbose_name="最高温度")
    min_temperature = models.IntegerField(verbose_name="最低温度")
    weather = models.CharField(verbose_name="天气", max_length=128)
    wind_direction = models.CharField(verbose_name="风向", max_length=128)
    # editable=False表示前后端不能被编辑
    week = models.CharField(verbose_name="星期", max_length=128,blank=True)
    # blank=True表示可以为空,后台填写的时候可以空着

    def __str__(self):
        return f"{self.date} - {self.week}"
        
    
        # admin 点击进去展示信息 以上操作相当于给objects命名

   
