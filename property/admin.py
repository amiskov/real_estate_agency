from django.contrib import admin

from .models import Flat, Complaint, Owner


class OwnerInline(admin.TabularInline):
    model = Owner.owned_flats.through
    raw_id_fields = ('owner',)
    extra = 0
    verbose_name = 'Собственник'
    verbose_name_plural = 'Собственники'
    model.owner.field.verbose_name = 'Собственник'
    model.__str__ = lambda _: 'Идентификатор собственника'


class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'town_district', 'address', 'owner')
    readonly_fields = ('created_at',)
    raw_id_fields = ('liked_by',)

    list_display = ('address', 'price', 'new_building', 'owners_phonenumber',
                    'owner_pure_phone', 'construction_year', 'town')
    list_editable = ('new_building',)
    list_filter = ('new_building', 'rooms_number', 'has_balcony')

    inlines = [OwnerInline]
    exclude = ["owners"]


class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('flat',)


class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('owned_flats',)
    list_display = ('full_name', 'pure_phone', 'get_owned_flats')

    def get_owned_flats(self, owner):
        return [flat.address for flat in owner.owned_flats.all()]
    get_owned_flats.short_description = 'Квартиры в собственности'


admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Owner, OwnerAdmin)
