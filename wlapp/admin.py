from django.contrib import admin
from wlapp.models import TianQiData,OrderData

class TianQiDataAdmin(admin.ModelAdmin):
    readonly_fields=('date','week')
    list_display = ('date','weather','max_temperature','min_temperature','wind_direction','week')
    list_filter = ('date','weather','max_temperature','min_temperature','wind_direction','week')
    search_fields = ('date','weather','max_temperature','min_temperature','wind_direction','week')
    list_per_page = 10
    ordering = ('date',)
# Register your models here.
# 功能 管理数据表
admin.site.register(TianQiData,TianQiDataAdmin)
admin.site.register(OrderData)


