# Generated by Django 3.2.16 on 2024-06-27 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240603_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('created_at',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('created_at',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'default_related_name': 'posts', 'ordering': ('-pub_date', 'created_at'), 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
