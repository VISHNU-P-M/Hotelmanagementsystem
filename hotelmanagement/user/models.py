from django.db import models
from django.contrib.auth.models import User, auth
from admin1.models import *
from datetime import date


# Create your models here.


class Details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    Id_proof = models.ImageField(null='True',upload_to='pics')

    @property
    def ImageURL(self):
        try:
            url= self.Id_proof.url
        except:
            url=''
        return url


class BookRoom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(RoomOverView,on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    no_of_room = models.IntegerField(null=True)
    no_of_guest = models.IntegerField(null=True)
    pay_status = models.BooleanField(null=True)
    checked_out = models.BooleanField(null=True,default=False)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    block = models.BooleanField(default=False,null=True)
    
    @property
    def is_past_due(self):
        return date.today() > self.check_out

    @property
    def is_checked_out(self):
        return date.today() < self.check_in

class Review(models.Model):
    book = models.OneToOneField(BookRoom,on_delete=models.CASCADE)
    review = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    