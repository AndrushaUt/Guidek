# Generated by Django 4.1.3 on 2023-05-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0004_post_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('author', models.CharField(max_length=100)),
                ('to_post', models.IntegerField()),
            ],
        ),
    ]