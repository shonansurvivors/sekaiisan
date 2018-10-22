from django.contrib import admin
from .models import Article, Heritage, Country, Blog, SiteMaster

admin.site.register(Article)
admin.site.register(Heritage)
admin.site.register(Country)
admin.site.register(Blog)
admin.site.register(SiteMaster)

