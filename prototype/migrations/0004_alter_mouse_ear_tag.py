# Generated by Django 4.0.3 on 2022-04-03 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0003_alter_measurement_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mouse',
            name='ear_tag',
            field=models.CharField(choices=[('N', 'N'), ('R', 'R'), ('L', 'L'), ('B', 'B'), ('RR', 'Rr'), ('LL', 'Ll'), ('BB', 'Bb')], max_length=2),
        ),
    ]