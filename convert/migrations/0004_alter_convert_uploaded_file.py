# Generated by Django 4.2 on 2023-05-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0003_alter_convert_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convert',
            name='uploaded_file',
            field=models.TextField(null=True),
        ),
    ]
