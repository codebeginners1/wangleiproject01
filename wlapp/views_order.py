import os 
from django.shortcuts import render,redirect
from django.http import HttpResponse
from wlapp.forms import OrderUploadForm,OrderQueryForm
from django.conf import settings
import pandas as pd
from wlapp.models import OrderData
import time

def order_manage(request):
    datas = OrderData.objects.all().order_by("-id")
    # 从数据库中获取所有的订单信息
    if request.method == "GET":
        form = OrderUploadForm()
    else:
        form = OrderUploadForm(request.POST,request.FILES)
        # key是form的名字,value是文件对象
        if form.is_valid():
            order_file = request.FILES.get("order_file")
            #"order_file"的是来自于OrderUploadForm的名字
            # order_file是一个文件对象
            # 保存文件到本地
            f_path = os.path.join(settings.MEDIA_ROOT,order_file.name)
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            with open(f_path,'wb') as f:
                for chunk in order_file.chunks():
                    f.write(chunk)
# 对文件进行迭代，产生给定大小的“块”。chunk_size 默认为 64KB。

# 这对非常大的文件特别有用，因为它允许将它们从磁盘上串联起来，避免将整个文件存储在内存中。
            return HttpResponse("上传成功")

    return render(request,'order_manage.html',{'form':form,"datas":datas}) 

def order_manage1(request):
    # 从数据库中获取所有的订单信息
    datas = OrderData.objects.all().order_by("-order_id")
    # 先初始化
    form = OrderUploadForm()
    formQuery = OrderQueryForm()
    if request.method == "POST":
        
        # key是form的名字,value是文件对象
        # 前端传进来sumit的name 进行校验
        if "formSubmitImport" in request.POST: 
            # 前端的button一定不能出错
            form = OrderUploadForm(request.POST,request.FILES)
            if form.is_valid():
                # 构造的时候进行校验，所以放进来if下面
                order_file = request.FILES.get("order_file")
                #"order_file"的是来自于form的sOrderUploadForm的名字
                # order_file是一个文件对象
                # 保存文件
                df=pd.read_excel(order_file)
                save_to_order_table(df)
                f_path = os.path.join(settings.MEDIA_ROOT,order_file.name)
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)
                with open(f_path,'wb') as f:
                    for chunk in order_file.chunks():
                        f.write(chunk)
           # 对文件进行迭代，产生给定大小的“块”。chunk_size 默认为 64KB。

# 这对非常大的文件特别有用，因为它允许将它们从磁盘上串联起来，避免将整个文件存储在内存中。
                return redirect("/order_manage/")
        

        if "formSubmitQuery" in request.POST or "formSubmitDownload" in request.POST:
            formQuery = OrderQueryForm(request.POST)
            if formQuery.is_valid():
                product_name = formQuery.cleaned_data.get("product_name")
                datas = datas.filter(product_name=product_name)
                # 这里是对数据库进行查询

                if "formSubmitDownload" in request.POST:
                    print(datas.values())
                    # 可以将数据数据变为dataframe
                    df =pd.DataFrame.from_records(datas.values())
                    curtime = int(time.time())

                    filename=f"order_{curtime}.csv"
                    response=HttpResponse(content_type="text/csv")
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    # 设置响应头 Content-Disposition，指示浏览器将响应内容作为附件下载，并使用生成的文件名
                    df.to_csv(path_or_buf=response,index=False)
                    return response




    return render(request,'order_manage1.html',{'form':form,"datas":datas,
                                                "formQuery":formQuery})

    


def save_to_order_table(df:pd.DataFrame):
    """
    df:pd.DataFrame类型声明
    """

    for ID,row in df.iterrows():
        db_datas = OrderData.objects.filter(order_id=row["单号"])
        if len(db_datas)>0:
            continue
        order_id = row["单号"]
        product_name = row["产品名称"]
        cost_price = row["成本价"]
        sale_price = row["销售价"]
        sale_num = row["销售数量"]
        product_cost = row["产品成本"]
        sale_income = row["销售收入"]
        sale_profit = row["销售利润"]

        OrderData.objects.create(order_id=order_id,
                                product_name=product_name,
                                cost_price=cost_price,
                                sale_price=sale_price,
                                sale_num=sale_num,
                                product_cost=product_cost,
                                sale_income=sale_income,
                                sale_profit=sale_profit)