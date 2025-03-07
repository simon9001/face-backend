# Generated by Django 5.1.6 on 2025-03-05 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images/')),
                ('blacklisted', models.BooleanField(default=False)),
                ('watchlisted', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('student', 'Student'), ('lecturer', 'Lecturer'), ('worker', 'Worker'), ('security', 'Security'), ('visitor', 'Visitor')], default='student', max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images/')),
                ('blacklisted', models.BooleanField(default=False)),
                ('watchlisted', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('visit_reason', models.TextField(blank=True, null=True)),
                ('visit_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
