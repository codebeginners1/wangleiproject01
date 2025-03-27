from django.shortcuts import render ,redirect
from django.http import HttpResponse,JsonResponse
from wlapp.forms import TianqiUploadForm
import pandas as pd
from wlapp.models import TianQiData
from django.db import connection
def tianqi_manage(request):
    # return HttpResponse("天气分析")
    years = get_all_year()
    form = TianqiUploadForm()
    if request.method == 'POST':
        form = TianqiUploadForm(request.POST,request.FILES)
        if form.is_valid():
            tianqi_file = request.FILES.get('tianqi_file')
            if ".xlsx" not in tianqi_file.name:
                form.add_error(None,"请上传xlsx格式的文件")
                return JsonResponse({'status':False,'error':dict(form.errors.items())})
                # 此刻用的是ajax，所以返回前端json，而非HttpResponse
            df = pd.read_excel(tianqi_file)
            save_to_tianqi_table(df)
            return JsonResponse({'status':True})
    return render(request,'tianqi_manage.html',{'form':form,"years":years})

def save_to_tianqi_table(df:pd.DataFrame):
    """
        '日期', '最高温度', '最低温度', '天气', '风力风向', '星期'
    date = models.DateField(verbose_name="日期")
    max_temperature = models.IntegerField(verbose_name="最高温度")
    min_temperature = models.IntegerField(verbose_name="最低温度")
    weather = models.CharField(verbose_name="天气", max_length=128)
    wind_direction = models.CharField(verbose_name="风向", max_length=128)
    week = models.CharField(verbose_name="风力", max_length=128)
    """

    for ID,row in df.iterrows():
        db_datas = TianQiData.objects.filter(date=row["日期"])
        if len(db_datas)>0:
            continue
        date = row["日期"]
        max_temperature = row["最高温"]
        min_temperature = row["最低温"]
        weather = row["天气"]
        wind_direction= row["风力风向"]
        week = row["星期"]
        

        TianQiData.objects.create(date = date,
                                max_temperature = max_temperature,
                                min_temperature = min_temperature,
                                weather = weather,
                                wind_direction= wind_direction,
                                week = week)



def get_all_year():
    sql = "select distinct year(date) from wlapp_tianqidata"
    years = set()
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            years.add(row[0])
    years=sorted(list(years))
    return years


def get_year_table(request):
    year = request.GET.get("year")
    sql  = "select * from wlapp_tianqidata where date like '%s%%' " % year
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = [x[0] for x in cursor.description]
    df.drop(["id"],axis=1,inplace=True)
    # 不显示id列
    return HttpResponse(df.to_html(index=False,classes="table table-bordered"))
# classes由bootstrap加样式


def get_tianqi_line(request):
    year = request.GET.get("year")
    sql  = "select * from wlapp_tianqidata where date like '%s%%' " % year
    colunms = []
    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = [x[0] for x in cursor.description]
    x=df["date"]
    y1=df["max_temperature"]
    y2=df["min_temperature"]

    return JsonResponse({"x":list(x),"y1":list(y1),"y2":list(y2)})

    
def get_tianqi_bar(request):
    year = request.GET.get("year")
    sql  = "select week,round(stddev(max_temperature),2) as stddev_maxTemperature from wlapp_tianqidata where date like '%s%%' group by week order by week " % year
    colunms = []
    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    df.columns = [x[0] for x in cursor.description]
    x=df["week"]
    y=df["stddev_maxTemperature"]
    return JsonResponse({"x":list(x),"y":list(y)})

def get_tianqi_pie(request):
    year = request.GET.get("year")
    sql = "select weather, count(*) as weather_count from wlapp_tianqidata where date like '%s%%' group by weather" % year
    rows = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    # 不会显示列名
    df.columns = [x[0] for x in cursor.description]
    df1 = df.sort_values(by="weather_count",ascending=False)[:8]
    data = [{"value": row.weather_count,"name": row.weather} for row in df1.itertuples()]
    return JsonResponse({"data": data})
        

