from django.contrib import admin
from .models import HouseModel, HouseInfo, Image


class ModelsAdmin(admin.ModelAdmin):
    pass


class HouseAdmin(admin.ModelAdmin):
    list_display = ('id','house_id', 'title', 'price', 'house_info', 'Host','type')
    search_fields = ('title','house_id')
    list_filter = ('Host',)


admin.site.register(HouseModel, HouseAdmin)
admin.site.register(HouseInfo, ModelsAdmin)
admin.site.register(Image, ModelsAdmin)
