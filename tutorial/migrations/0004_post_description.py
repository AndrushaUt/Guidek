# Generated by Django 4.1.3 on 2023-01-07 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0003_alter_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default='t', max_length=200),
            preserve_default=False,
        ),
    ]
