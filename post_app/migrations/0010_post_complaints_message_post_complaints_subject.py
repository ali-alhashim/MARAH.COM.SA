# Generated by Django 4.1.6 on 2023-09-05 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0009_post_complaints'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_complaints',
            name='message',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='post_complaints',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
