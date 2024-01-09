from django.contrib import admin

from apps.ubigeous.models import Region, Province, District, User


# ** Defining the models for the django administrator
# * Region, Province and District models will be ordered by their 'name' field
class RegionAdmin(admin.ModelAdmin):
    ordering = ('name',)


class ProvinceAdmin(admin.ModelAdmin):
    ordering = ('name',)


class DistrictAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(User)
admin.site.register(Region, RegionAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
