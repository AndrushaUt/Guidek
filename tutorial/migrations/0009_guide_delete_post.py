# Generated by Django 4.1.3 on 2023-05-24 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0008_alter_post_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('description', models.TextField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('date', models.DateField()),
                ('username', models.CharField(max_length=150)),
                ('likes_amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
