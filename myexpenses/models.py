from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50)
    comments = models.CharField(max_length = 2000)
    created = models.DateTimeField(auto_now=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):

    TRANSACTION_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]

    name = models.CharField(max_length = 50)
    type = models.CharField(choices=TRANSACTION_CHOICES, default='expense', max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_for = models.CharField(max_length = 200)
    paid_by = models.CharField(max_length=20)
    paid_to = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    comments = models.CharField(max_length = 2000)
    date = models.DateField(blank=False)
    created = models.DateTimeField(auto_now=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return self.name
