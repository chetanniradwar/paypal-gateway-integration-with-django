from django.db import models

# Create your models here.

class donor(models.Model):
    email_id=models.CharField(max_length=50,unique=True)
    first_name =models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
   
    mobile_no =models.IntegerField()

class transaction(models.Model):
    donor = models.ForeignKey(donor, on_delete=models.CASCADE)
    order_id=models.CharField(max_length=50)
    amount_val=models.IntegerField()
    trans_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50)



