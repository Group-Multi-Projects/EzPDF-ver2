# Generated by Django 4.2.6 on 2024-08-02 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('File', '0005_alter_filemodel_file_format'),
        ('tools', '0002_drawmodel_item_id_textmodel_item_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField(verbose_name='Page Number')),
                ('tool_type', models.CharField(default='Draw', max_length=20, verbose_name='Tool Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('item_id', models.CharField(max_length=200, null=True)),
                ('image', models.ImageField(upload_to='media/edit_images/')),
                ('coord_in_canvas_X', models.FloatField(verbose_name='Canvas X Coordinate')),
                ('coord_in_canvas_Y', models.FloatField(verbose_name='Canvas Y Coordinate')),
                ('coord_in_doc_X', models.FloatField(verbose_name='Document X Coordinate')),
                ('coord_in_doc_Y', models.FloatField(verbose_name='Document Y Coordinate')),
                ('height', models.FloatField(verbose_name='Image height')),
                ('width', models.FloatField(verbose_name='Image width')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='File.filemodel', verbose_name='File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeometryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField(verbose_name='Page Number')),
                ('tool_type', models.CharField(default='Draw', max_length=20, verbose_name='Tool Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('item_id', models.CharField(max_length=200, null=True)),
                ('coord_in_canvas_X', models.FloatField(verbose_name='Canvas X Coordinate')),
                ('coord_in_canvas_Y', models.FloatField(verbose_name='Canvas Y Coordinate')),
                ('coord_in_doc_X', models.FloatField(verbose_name='Document X Coordinate')),
                ('coord_in_doc_Y', models.FloatField(verbose_name='Document Y Coordinate')),
                ('height', models.FloatField(verbose_name='Geometry height')),
                ('width', models.FloatField(verbose_name='Geometry width')),
                ('color', models.CharField(max_length=20)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='File.filemodel', verbose_name='File')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]