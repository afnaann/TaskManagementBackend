# Generated by Django 5.1.1 on 2024-09-30 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_usertasks_delete_assigntasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='all_completed',
            field=models.BooleanField(default=False),
        ),
    ]
