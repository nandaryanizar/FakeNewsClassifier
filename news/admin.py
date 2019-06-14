from django.contrib import admin
from .models import News, NewsPredictionFeedback

# Register your models here.
admin.site.register(News)
admin.site.register(NewsPredictionFeedback)