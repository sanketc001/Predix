# Generated by Django 3.2.9 on 2021-11-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mid', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.CharField(blank=True, max_length=5, null=True)),
                ('ranking', models.CharField(blank=True, max_length=5, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('genre', models.JSONField(blank=True, null=True)),
                ('rdate', models.CharField(blank=True, max_length=50, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('language', models.JSONField(blank=True, null=True)),
                ('cover', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('trailer', models.CharField(blank=True, max_length=255, null=True)),
                ('released', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
    ]
