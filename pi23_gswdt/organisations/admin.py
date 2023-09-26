from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Domain, Organisation


@admin.register(Organisation)
class OrganisationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "tenant_type", "is_enabled", "in_production")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "created", "modified")
