# Generated by Django 5.0.4 on 2024-07-18 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_workshop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtask',
            name='assigned',
        ),
        migrations.RemoveField(
            model_name='task',
            name='assigned',
        ),
        migrations.AddField(
            model_name='subtask',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_assign', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user_assign', to=settings.AUTH_USER_MODEL),
        ),
    ]
