from django.contrib import admin

from src.adminauction.models import FeeArticle
from src.adminauction.models import SetBidArticle
from src.adminauction.models import UserPermission

admin.site.register(SetBidArticle)
admin.site.register(FeeArticle)
admin.site.register(UserPermission)
