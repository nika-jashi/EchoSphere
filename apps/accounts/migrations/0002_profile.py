# Generated by Django 5.0 on 2024-01-04 13:59

import apps.accounts.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('date_of_birth', models.DateField()),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(upload_to=apps.accounts.models.profile_picture_file_path)),
                ('gender', models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='U')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
