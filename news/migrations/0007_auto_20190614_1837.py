# Generated by Django 2.2.2 on 2019-06-14 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20190614_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspredictionfeedback',
            name='client',
            field=models.ForeignKey(db_column='client_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='prediction_feedbacks', to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL, to_field='client_id'),
        ),
        migrations.AlterField(
            model_name='newspredictionfeedback',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_feedbacks', to='news.News'),
        ),
    ]
