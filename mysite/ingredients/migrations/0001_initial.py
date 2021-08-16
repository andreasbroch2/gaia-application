# Generated by Django 3.2.6 on 2021-08-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('type', models.TextField()),
                ('price', models.TextField()),
                ('summary', models.TextField(default='This is cool')),
            ],
        ),
    ]