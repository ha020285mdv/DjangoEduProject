# Generated by Django 4.0.4 on 2022-06-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_comment_content_type_comment_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='type',
            field=models.CharField(choices=[('L', 'Like'), ('D', 'Dislike')], default='L', max_length=1),
        ),
    ]