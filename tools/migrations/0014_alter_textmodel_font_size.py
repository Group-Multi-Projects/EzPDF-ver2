# Generated by Django 4.2.6 on 2024-08-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0013_textmodel_font_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmodel',
            name='font_size',
            field=models.CharField(default=12, max_length=20, null=True, verbose_name='Font Size'),
        ),
    ]
