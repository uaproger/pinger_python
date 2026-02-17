import requests
from celery import shared_task
from .models import Service


@shared_task
def check_all_services_cron():
    services = Service.objects.all()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }

    for service in services:
        try:
            response = requests.get(service.url, timeout=10, headers=headers, allow_redirects=True)
            service.status_code = response.status_code
            service.is_online = (200 <= response.status_code < 400)
        except Exception as e:
            service.status_code = 0
            service.is_online = False

        service.save()
    return f"Checked {services.count()} services."
