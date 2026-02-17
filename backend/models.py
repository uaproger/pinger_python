from django.db import models
from django.conf import settings


class Service(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    last_check = models.DateTimeField(auto_now=True)
