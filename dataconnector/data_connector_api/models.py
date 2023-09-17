from django.db import models

class Trade(models.Model):
    userName = models.CharField(max_length=255)
    actions = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    quantity = models.IntegerField()
    type = models.CharField(max_length=255)
    price_status = models.DecimalField(max_digits=10, decimal_places=4)
    fee = models.DecimalField(max_digits=5, decimal_places=2)
    date_time = models.DateTimeField()