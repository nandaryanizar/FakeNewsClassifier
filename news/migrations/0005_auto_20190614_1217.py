# Generated by Django 2.2.2 on 2019-06-14 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190614_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspredictionfeedback',
            name='client',
            field=models.ForeignKey(db_column='client_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='client', to=settings.OAUTH2_PROVIDER_APPLICATION_MODEL, to_field='client_id'),
        ),
    ]