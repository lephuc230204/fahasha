# Generated by Django 5.0.3 on 2024-04-11 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='profile_picture',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]
