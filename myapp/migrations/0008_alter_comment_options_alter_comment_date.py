# Generated by Django 4.0.4 on 2022-06-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_like_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id'], 'verbose_name': '3_Comment'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
