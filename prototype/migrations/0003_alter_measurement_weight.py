# Generated by Django 4.0.3 on 2022-03-18 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0002_rename_expirementgroup_experimentgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
