from django.contrib import admin
from .models import Goods, UploadedFile
# Register your models here.

admin.site.register(Goods)
admin.site.register(UploadedFile)
