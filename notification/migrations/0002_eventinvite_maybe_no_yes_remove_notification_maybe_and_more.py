# Generated by Django 4.1.1 on 2022-09-15 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_alter_replies_comment'),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maybe', models.ManyToManyField(related_name='maybe_members', to='groups.member')),
                ('no', models.ManyToManyField(related_name='no_members', to='groups.member')),
                ('yes', models.ManyToManyField(related_name='yes_members', to='groups.member')),
            ],
        ),
        migrations.CreateModel(
            name='Maybe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.member')),
            ],
        ),
        migrations.CreateModel(
            name='No',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.member')),
            ],
        ),
        migrations.CreateModel(
            name='Yes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.member')),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='maybe',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='no',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='yes',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
