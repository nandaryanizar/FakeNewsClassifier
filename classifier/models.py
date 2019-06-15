from django.db import models
from django.utils import timezone

class Classifier(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    last_train_at = models.DateTimeField(default=timezone.now)