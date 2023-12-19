from django.db import models
from manas_codes.users.models import User


# Create your models here.
class Category(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    name = models.CharField(max_length=50)
    comments = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    # created = models.DateTimeField(blank=True)
    # updated = models.DateTimeField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Group(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    name = models.CharField(max_length=50, default="Hyderabad Home")
    comments = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    TRANSACTION_CHOICES = [("expense", "Expense"), ("income", "Income")]

    # def get_default_group():
    #     return Group.objects.get_or_create(name="Hyderabad Home")[0].id

    # def get_default_user():
    #     return User.objects.get_or_create(username="manas")[0].id

    name = models.CharField(max_length=50)
    type = models.CharField(
        choices=TRANSACTION_CHOICES, default="expense", max_length=10
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_for = models.CharField(max_length=200)
    paid_by = models.CharField(max_length=20)
    paid_to = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        blank=True
        # , default=get_default_group
    )
    comments = models.CharField(max_length=2000)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
        # , default=get_default_user
    )
    date = models.DateField(blank=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    # created = models.DateTimeField(blank=True)
    # updated = models.DateTimeField(blank=True)

    def __str__(self) -> str:
        return self.name
