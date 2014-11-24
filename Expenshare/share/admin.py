from django.contrib import admin
from share.models import PayGroup, PaymentLog, PayUser, MemberView, FellowUser
# Register your models here.

admin.site.register(PayGroup)
admin.site.register(PaymentLog)
admin.site.register(PayUser)
admin.site.register(FellowUser)
admin.site.register(MemberView)