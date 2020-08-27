from django.contrib import admin
from .models import HouseModel, HouseInfo, Image, ClientViewSet


class ModelsAdmin(admin.ModelAdmin):
    pass


class HouseAdmin(admin.ModelAdmin):
    list_display = ('id','house_id', 'title', 'price', 'house_info', 'Host','type')
    search_fields = ('title','house_id')
    list_filter = ('Host','offer_type', 'type')


admin.site.register(HouseModel, HouseAdmin)
admin.site.register(HouseInfo, ModelsAdmin)
admin.site.register(ClientViewSet, ModelsAdmin)
admin.site.register(Image, ModelsAdmin)
