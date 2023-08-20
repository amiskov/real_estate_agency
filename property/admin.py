from django.contrib import admin

from .models import Flat


class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'town_district', 'address', 'owner']
    readonly_fields = ['created_at']


admin.site.register(Flat, FlatAdmin)
