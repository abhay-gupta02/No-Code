# Generated by Django 5.1.6 on 2025-02-25 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0006_submenu'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=100, unique=True)),
                ('menu_url', models.CharField(blank=True, max_length=200, null=True)),
                ('display_order', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
