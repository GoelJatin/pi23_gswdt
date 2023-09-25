from django.db import models


class AccountTypeChoices(models.TextChoices):
    SAVINGS = "savings"
    CURRENT = "current"
    LOAN = "loan"
    OTHER = "other"
