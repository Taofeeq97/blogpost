# Generated by Django 4.2 on 2023-04-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_rename_no_views_post_no_of_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='no_of_views',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]