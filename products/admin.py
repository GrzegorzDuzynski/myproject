from django.contrib import admin

from products.models import (
    Type,
    NewUser,
    Product,
    Status,
    Section)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin): ...


@admin.register(NewUser)
class MyUserAdmin(admin.ModelAdmin): ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): ...


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin): ...


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin): ...
