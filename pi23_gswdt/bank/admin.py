from django.contrib import admin

from .models import Account, AccountType, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
