# Generated by Django 4.1.3 on 2023-01-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
