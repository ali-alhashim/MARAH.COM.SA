# Generated by Django 4.1.6 on 2023-09-02 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_alter_usermessage_options_usermessagereply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermessagereply',
            options={'ordering': ['-sent_date']},
        ),
        migrations.RemoveField(
            model_name='user',
            name='fcm_token',
        ),
        migrations.AlterField(
            model_name='usermessagereply',
            name='reply_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='message_replies', to='user_app.usermessage'),
        ),
    ]
