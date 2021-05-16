from django.contrib import admin

# Register your models here.
from .models import donor
from .models import transaction

admin.site.register(donor)
admin.site.register(transaction)