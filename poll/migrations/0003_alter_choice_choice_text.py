# Generated by Django 4.1.1 on 2022-09-10 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_alter_poll_end_date_alter_poll_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]