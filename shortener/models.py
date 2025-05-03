import random
import string
from django.db import models

def generate_shortcode():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortURL(models.Model):
    url = models.URLField()
    shortcode = models.CharField(max_length=15, unique=True, default=generate_shortcode)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shortcode} -> {self.url}"
