from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model



admin.site.register(Person)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Book_Category)
