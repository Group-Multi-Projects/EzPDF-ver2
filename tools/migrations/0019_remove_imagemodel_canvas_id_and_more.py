# Generated by Django 4.2.6 on 2024-08-15 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0018_remove_textmodel_coord_in_doc_x_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='canvas_id',
        ),
        migrations.RemoveField(
            model_name='imagemodel',
            name='coord_in_doc_X',
        ),
        migrations.RemoveField(
            model_name='imagemodel',
            name='coord_in_doc_Y',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='angle',
            field=models.FloatField(null=True, verbose_name='Angle'),
        ),
    ]