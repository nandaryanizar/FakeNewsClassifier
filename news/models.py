from django.db import models
from django.utils import timezone

from oauth2_provider.models import Application

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    preprocessed_content = models.TextField()
    author = models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    is_fake_news = models.BooleanField()
    total_is_fake_feedback = models.IntegerField()
    total_is_not_fake_feedback = models.IntegerField()
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

class NewsPredictionFeedback(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='prediction_feedbacks')
    client = models.ForeignKey(Application, to_field='client_id', db_column='client_id', on_delete=models.DO_NOTHING, related_name='prediction_feedbacks')
    is_fake_news = models.BooleanField()

