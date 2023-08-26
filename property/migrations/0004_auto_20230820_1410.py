# Generated by Django 2.2.24 on 2023-08-20 11:10

from django.db import migrations


def fill_new_building_field(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    # По умолчанию поле `new_building` имеет значение `None`.
    # Case/When я применил, чтобы расставить и True и False одним запросом,
    # т.к. логично не оставлять `None`-значения для `new_building`.
    # Flat.objects.update(new_building=Case(
    #     When(construction_year__gte='2015', then=True),
    #     default=False))

    # Через filter+update в этой версии Django я вижу способ такое сделать
    # только двумя запросами:
    Flat.objects.filter(construction_year__gte=2015) \
        .update(new_building=True)
    Flat.objects.filter(construction_year__lt=2015) \
        .update(new_building=False)
    # думал использовать что-то типа `F('construction_year') >= 2015`, но он не
    # поддерживает операторы сравнения...



def reset_new_building_field(apps, schema_editor):
    """Set all `new_building` fields to `False`."""
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.update(new_building=None)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_flat_new_building'),
    ]

    operations = [
        migrations.RunPython(fill_new_building_field,
                             reset_new_building_field),
    ]
