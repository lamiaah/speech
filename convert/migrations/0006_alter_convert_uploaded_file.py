# Generated by Django 4.2 on 2023-05-19 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0005_alter_convert_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convert',
            name='uploaded_file',
            field=models.FileField(null=True, upload_to='audio_file'),
        ),
    ]