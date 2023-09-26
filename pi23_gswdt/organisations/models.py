from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin, TenantMixin
from django_tenants.utils import get_tenant_type_choices
from model_utils.models import TimeStampedModel, UUIDModel


class Organisation(TimeStampedModel, UUIDModel, TenantMixin):
    name = models.CharField(_("Author name"), max_length=50)
    tenant_type = models.CharField(max_length=100, choices=get_tenant_type_choices())
    is_enabled = models.BooleanField(_("Is Tenant Enabled?"))
    in_production = models.BooleanField(_("Is Tenant Live in Production?"))

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(TimeStampedModel, UUIDModel, DomainMixin):
    @staticmethod
    def standard_domain_from_schema_name(schema_name):
        return f"{schema_name.lower()}.{settings.BASE_URL}"

    def clean(self):
        if settings.BASE_URL not in self.domain or len(self.domain) == len(settings.BASE_URL):
            raise ValidationError(
                "Subdomain and BASE_URL must be included in the url if a custom domain "
                f"is not being used. ie; <subdomain>.{settings.BASE_URL}"
            )
