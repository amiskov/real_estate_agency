from django.contrib import admin

from .models import Flat, Complaint, Owner

admin.site.site_header = 'Агентство недвижимости'
admin.site.site_title = 'Агентство недвижимости'


class OwnerInline(admin.TabularInline):
    model = Owner.flats.through
    raw_id_fields = ('owner',)
    extra = 0
    verbose_name = 'Собственник'
    verbose_name_plural = 'Собственники'
    model.owner.field.verbose_name = 'Собственник'
    model.__str__ = lambda _: 'Идентификатор собственника'


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'town_district', 'address', 'owners__full_name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('liked_by',)

    list_display = ('id', 'address', 'price', 'new_building',
                    'get_owners_phonenumbers', 'get_owners_pure_phones',
                    'construction_year', 'town')
    list_editable = ('new_building',)
    list_filter = ('new_building', 'rooms_number', 'has_balcony')

    inlines = [OwnerInline]
    exclude = ["owners"]

    def get_owners_phonenumbers(self, flat):
        phonenumbers = [str(owner.phonenumber) for owner in flat.owners.all()]
        return ", ".join(phonenumbers)

    def get_owners_pure_phones(self, flat):
        pure_phones = [str(owner.pure_phone) for owner in flat.owners.all()]
        return ", ".join(pure_phones)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('flat',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('flats',)
    list_display = ('full_name', 'pure_phone', 'get_flats')

    def get_flats(self, owner):
        return [flat.address for flat in owner.flats.all()]
    get_flats.short_description = 'Квартиры в собственности'
