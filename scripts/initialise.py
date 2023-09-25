import random

from django.conf import settings
from django.contrib.auth import get_user_model

from pi23_gswdt.bank.models import Account, AccountType, AccountTypeChoices, Customer

User = get_user_model()


def create_superuser():
    try:
        global_superuser = User.objects.create_superuser(
            name="Jatin Goel",
            username="jatin",
            email="jatingoel1037@gmail.com",
            password="qwerty123",
            is_superuser=True,
            is_staff=True,
        )

        print("Created user: ", global_superuser)
    except Exception as excp:
        print(f"Failed to create user, error: [{excp}]")


def create_customers():
    customers = [
        {"cust_id": 123456781, "name": "Jatin 1", "email": "jatin@1.com"},
        {"cust_id": 123456782, "name": "Jatin 2", "email": "jatin@2.com"},
        {"cust_id": 123456783, "name": "Jatin 3", "email": "jatin@3.com"},
        {"cust_id": 123456784, "name": "Jatin 4", "email": "jatin@4.com"},
        {"cust_id": 123456785, "name": "Jatin 5", "email": "jatin@5.com"},
    ]

    obj_set = []

    for customer in customers:
        obj_set.append(Customer(**customer))

    try:
        Customer.objects.bulk_create(obj_set)
    except Exception as excp:
        print(f"Customer creation failed. Error: [{excp}]")
        return

    print("Customer creation successful !!!!")


def create_account_types():
    obj_set = []

    for account_type in AccountTypeChoices.values:
        obj_set.append(AccountType(account_type=account_type))

    try:
        AccountType.objects.bulk_create(obj_set)
    except Exception as excp:
        print(f"Account Type creation failed. Error: [{excp}]")
        return

    print("Account Type creation successful !!!!")


def create_accounts():
    obj_set = []

    for customer in Customer.objects.all():
        for _ in range(2):
            obj_set.append(
                Account(
                    customer=customer,
                    account_type=random.choice(AccountType.objects.all()),
                    account_number=random.randint(10**15, 10**16 - 1),
                    balance=random.randint(100, 10**4),
                )
            )

    try:
        Account.objects.bulk_create(obj_set)
    except Exception as excp:
        print(f"Account creation failed. Error: [{excp}]")
        return

    print("Account creation successful !!!!")


def run(*args):
    create_superuser()
    create_customers()
    create_account_types()
    create_accounts()
