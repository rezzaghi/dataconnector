from django.utils import timezone
from datetime import datetime

def convert_date_time_format(date_str):
    datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_str = datetime_obj.strftime("%m/%d/%Y - %H:%M")
    datetime_obj = datetime.strptime(formatted_str, "%m/%d/%Y - %H:%M")
    return timezone.make_aware(datetime_obj)