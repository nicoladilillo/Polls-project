from django.contrib import admin

from .models import Question, Choice, Poll

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Poll)
