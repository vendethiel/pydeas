from django.contrib import admin

from .models import Category, Idea, Implementation

admin.site.register(Category)
admin.site.register(Idea)
admin.site.register(Implementation)