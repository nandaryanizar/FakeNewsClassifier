# Generated by Django 2.2.2 on 2019-06-14 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('preprocessed_content', models.TextField()),
                ('author', models.CharField(max_length=200)),
                ('created_by', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_fake_news', models.BooleanField()),
                ('total_is_fake_feedback', models.IntegerField()),
                ('total_is_not_fake_feedback', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NewsFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.BooleanField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.News')),
            ],
        ),
    ]