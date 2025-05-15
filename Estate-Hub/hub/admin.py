from django.contrib import admin
from .models import CustomUser,Listing
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Listing)
