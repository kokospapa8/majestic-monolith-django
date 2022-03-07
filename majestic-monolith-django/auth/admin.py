# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import PhonenumberCheck, AllowedPhonenumbers


@admin.register(PhonenumberCheck)
class PhonenumberCheckAdmin(admin.ModelAdmin):
    list_display = ['phonenumber', 'verified',
                    'timestamp_requested', 'timestamp_verified']
    search_fields = ['phonenumber', ]
    list_filter = ['verified']
    actions = ['delete_selected']


@admin.register(AllowedPhonenumbers)
class AllowedPhonenumbersAdmin(admin.ModelAdmin):
    list_display = ['phonenumber', 'description']
    search_fields = ['phonenumber']
    actions = ['delete_selected']
