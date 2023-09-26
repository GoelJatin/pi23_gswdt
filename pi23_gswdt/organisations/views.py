from django.db import connection
from django.http import HttpResponse
from django.utils import timezone


def current_datetime(request):
    now = timezone.now()
    html = f"<html><body>It is now {now} for tenant: [{connection.schema_name}]</body></html>"
    return HttpResponse(html)
