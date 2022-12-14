# Generated by Django 4.0.6 on 2022-08-02 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=80)),
                ('symbol', models.CharField(max_length=80)),
                ('dividend_Ex_Date', models.CharField(max_length=80)),
                ('payment_Date', models.CharField(max_length=80)),
                ('record_Date', models.CharField(max_length=80)),
                ('dividend_Rate', models.FloatField()),
                ('indicated_Annual_Dividend', models.FloatField()),
                ('announcement_Date', models.CharField(max_length=80)),
            ],
        ),
    ]
