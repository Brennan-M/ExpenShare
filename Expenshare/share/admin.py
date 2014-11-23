from django.contrib import admin
from share.models import PayGroup, PaymentLog, PayUser
# Register your models here.

admin.site.register(PayGroup)
admin.site.register(PaymentLog)
admin.site.register(PayUser)