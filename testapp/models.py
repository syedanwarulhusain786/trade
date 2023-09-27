from django.db import models

# Create your models here.


class Data(models.Model):
    ips= models.CharField(max_length=255)
    
    filename= models.CharField(max_length=255)
    back_pass = models.CharField(max_length=255)
    back_Result = models.CharField(max_length=255)
    back_Profit = models.CharField(max_length=255)
    back_Recovery_Factor = models.CharField(max_length=255)
    back_Equity_DD_d = models.CharField(max_length=255)
    back_Trades = models.CharField(max_length=255)
    forward_Forward_Result = models.CharField(max_length=255)
    forward_Profit = models.CharField(max_length=255)
    forward_Recovery_Factor = models.CharField(max_length=255)
    forward_Equity_DD_d = models.CharField(max_length=255)
    forward_Trades = models.CharField(max_length=255)
    profit_match = models.CharField(max_length=255)
    total_profit = models.CharField(max_length=255)
    max_original_dd = models.CharField(max_length=255)