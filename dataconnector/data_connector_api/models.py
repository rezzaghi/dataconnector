from django.db import models
from django.utils import timezone
from datetime import datetime

class TransactionManager(models.Manager):
    def record_data_collected(self, transaction_data, username):
        for item in transaction_data:
            date_format = "%m/%d/%Y - %H:%M"
            date_time = timezone.make_aware(datetime.strptime(item['date_time'], date_format))
            price_status = float(item['price_status'].replace('$', ''))

            # Ensure uniqueness of all fields
            criteria = {
                'userName': username,
                'actions': item['actions'],
                'transaction_type': item['transaction_type'],
                'symbol': item['symbol'],
                'quantity': item['quantity'],
                'type': item['type'],
                'price_status': price_status,
                'fee': item['fee'],
                'date_time': date_time,
            }
            # Check if a similar transaction already exists in the database
            existing_transaction = self.filter(**criteria).first()
            if not existing_transaction:
                self.create(
                    userName=username,
                    actions=item['actions'],
                    transaction_type=item['transaction_type'],
                    symbol=item['symbol'],
                    quantity=item['quantity'],
                    type=item['type'],
                    price_status=price_status,
                    fee=item['fee'],
                    date_time=date_time
                )
    
    def get_transactions_within_date_range(self, start_date, end_date, username):
        trades_within_range = self.filter(date_time__gte=start_date, date_time__lte=end_date, userName=username)
        formatted_data = []
        for trade in trades_within_range:
            formatted_data.append({
                "actions": trade.actions,
                "transaction_type": trade.transaction_type,
                "symbol": trade.symbol,
                "quantity": trade.quantity,
                "type": trade.type,
                "price_status": trade.price_status,
                "fee": trade.fee,
                "date_time": trade.date_time.strftime("%m/%d/%Y - %H:%M")
            })

        return formatted_data


class Transaction(models.Model):
    userName = models.CharField(max_length=255)
    actions = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    quantity = models.IntegerField()
    type = models.CharField(max_length=255)
    price_status = models.DecimalField(max_digits=10, decimal_places=4)
    fee = models.DecimalField(max_digits=5, decimal_places=2)
    date_time = models.DateTimeField()
    objects = TransactionManager()