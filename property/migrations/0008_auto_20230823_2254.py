# Generated by Django 2.2.24 on 2023-08-23 19:54

import phonenumbers
from logging import error
from django.db import migrations


def purify_phone_number(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    for flat in Flat.objects.all().iterator():
        parsed_phone = phonenumbers.parse(flat.owners_phonenumber, 'RU')
        if phonenumbers.is_valid_number(parsed_phone):
            flat.owner_pure_phone = parsed_phone
            flat.save()
        else:
            error(f'Failed parsing phone number {flat.owners_phonenumber}')


def reset_pure_phone_number_field(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.update(owner_pure_phone=None)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(purify_phone_number,
                             reset_pure_phone_number_field),
    ]
