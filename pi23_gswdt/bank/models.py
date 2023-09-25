from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel

from .constants import AccountTypeChoices


class Customer(UUIDModel, TimeStampedModel):
    cust_id = models.PositiveIntegerField(_("9 Digit customer ID"))
    name = models.CharField(_("Customer Name"), max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Customer: [{self.name} - {self.cust_id} - {self.email}]"


class AccountType(UUIDModel, TimeStampedModel):
    account_type = models.CharField(_("Type of Account"), unique=True, choices=AccountTypeChoices.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Account Type: [{self.account_type}]"


class Account(UUIDModel, TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    account_number = models.PositiveBigIntegerField(_("16 digit account number"))
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return (
            f"{self.customer.name}({self.customer.cust_id}) - {self.account_type.account_type} "
            f"Account: [{self.account_number}]"
        )
