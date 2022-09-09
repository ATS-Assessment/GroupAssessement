# Generated by Django 4.1.1 on 2022-09-09 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_rename_date_created_like_date_liked_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grouprequest',
            old_name='request_messgae',
            new_name='request_message',
        ),
        migrations.AlterField(
            model_name='member',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='replies',
            name='content',
            field=models.TextField(max_length=80),
        ),
    ]
