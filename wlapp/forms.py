#use wlproject;
# alter table wlapp_tiaqidata convert to character set utf8mb4;

from django import forms
from django.core.exceptions import ValidationError 
from wlapp.models import User,OrderData
from captcha.fields import CaptchaField
class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label="密码",widget=forms.PasswordInput,min_length=8,max_length=20)
    #借助选择不同的 widget，你能够控制表单字段在页面上的显示样式与交互方式。
    #不同的 widget 会生成不同类型的 HTML 输入元素，例如文本框、下拉框、复选框
    password_confirm = forms.CharField(label="密码确认",widget=forms.PasswordInput,min_length=8,max_length=20)
    # 与model不同
    gender_choices=[("1","男生"),("0","女生")]
    gender = forms.ChoiceField(label="性别",choices=gender_choices)
    role_choices=[("admin","管理员"),("normal","普通用户")]
    role = forms.ChoiceField(label="角色",choices=role_choices)
    age=forms.IntegerField(label="年龄",min_value=0,max_value=100)
    # 这个form到前端，展现的样式会很丑
    # 可以用 插件django-crispy-forms可以跟bootstrap很好完成样式对接
    # 但是这个插件需要单独安装
    def clean(self):
        # 校验函数
        # 函数名字也不能改，clean是所有字段的直接关系
        password=self.cleaned_data.get('password')
        password_confirm=self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("两次密码输入不一致")
        
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if username:
            username=username.strip()
        if not self.is_update:
        # 使用方法clean_变量名
            users=User.objects.filter(username=username)
            if len(users)>0:
                raise ValidationError(f"用户名{username}已存在")
        return username
    
    
    def set_update(self,update):
        self.is_update = update

        # 通过这个方法来检查更新与否
  
"""
  .form.is_valid() 方法会依次执行表单的字段级验证和全局验证（即 clean 方法）。
  示例如下：
"""





class UserModelForm(forms.ModelForm):
    password_confirm=forms.CharField(label="密码确认",widget=forms.PasswordInput,min_length=8,max_length=20)
    class Meta:
        # 定义类本身使用的model
        model = User

        fields=['username','password','password_confirm',
                'gender','role','age','head_img']
        # 但是这里并无create_time值
        # 使用User的这几个字段,但是ModelForm并不会识别密码字段，所有输入值会显示
        widgets={
            "password":forms.PasswordInput()

        }

    def clean(self):
        # 校验函数
        # 函数名字也不能改，clean是所有字段的直接关系
        password=self.cleaned_data.get('password')
        password_confirm=self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("两次密码输入不一致")
        
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if username:
            username=username.strip()
        if not self.is_update:
        # 使用方法clean_变量名
            users=User.objects.filter(username=username)
            if len(users)>0:
                raise ValidationError(f"用户名{username}已存在")
        return username
    
    def set_update(self,update):
        self.is_update = update


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",min_length=3,max_length=100)
    password = forms.CharField(label="密码",widget=forms.PasswordInput,min_length=3)
    captcha = CaptchaField(label="验证码")
    # 用于验证码的校验，会使得request.path中有captcha路径


class OrderUploadForm(forms.Form):
    order_file = forms.FileField(label="上传文件")


class OrderQueryForm(forms.Form):
    orders = OrderData.objects.values('product_name').distinct()
    # 从数据库中获取产品名称并且去重
    choices = [(order['product_name'],order['product_name']) for order in orders]
    product_name = forms.ChoiceField(label="产品名称",choices=choices)




class TianqiUploadForm(forms.Form):
    tianqi_file = forms.FileField(label="上传文件")
    

