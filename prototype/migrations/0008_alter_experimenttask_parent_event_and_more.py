# Generated by Django 4.0.3 on 2022-04-04 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0007_alter_experimenttask_parent_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimenttask',
            name='parent_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prototype.experimenttask'),
        ),
        migrations.AlterField(
            model_name='tumormeasurement',
            name='record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prototype.measurement'),
        ),
    ]
