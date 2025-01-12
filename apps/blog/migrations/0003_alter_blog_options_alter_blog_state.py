# Generated by Django 5.1.4 on 2025-01-12 15:08

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'Blog', 'verbose_name_plural': 'Blogs'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='state',
            field=django_fsm.FSMField(choices=[('draft', 'Draft'), ('published', 'Published'), ('edited', 'Edited'), ('archived', 'Archived')], default='draft', max_length=50),
        ),
    ]
