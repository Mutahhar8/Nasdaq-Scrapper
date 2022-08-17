from django.db import models


# Create your models here.


class Data(models.Model):
    companyName = models.CharField(max_length=80)
    symbol = models.CharField(max_length=80)
    dividend_Ex_Date = models.CharField(max_length=80)
    payment_Date = models.CharField(max_length=80)
    record_Date = models.CharField(max_length=80)
    dividend_Rate = models.FloatField()
    indicated_Annual_Dividend = models.FloatField()
    announcement_Date = models.CharField(max_length=80)

    def __str__(self):
        return self.symbol




