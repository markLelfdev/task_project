import time
from django.utils import timezone
from datetime import datetime

tz_bangkok = timezone.get_current_timezone()
    
def localize_time(dt):
    if dt:
        return dt.astimezone(tz_bangkok).strftime('%Y-%m-%d %H:%M:%S')
    return None