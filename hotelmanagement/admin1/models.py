from django.db import models
from datetime import date
from user.models import User

# Create your models here.
class Receptionist(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=150)

class Category(models.Model):
    category = models.CharField(max_length=20)

class Amenities(models.Model):
    amenities = models.CharField(max_length=20)

class RoomOverView(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE) 
    rooms = models.BigIntegerField()
    available = models.BigIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=2)

class RoomPic(models.Model):
    room = models.ForeignKey(RoomOverView,on_delete=models.CASCADE)
    pic = models.ImageField(null=True,upload_to='pics')

    @property
    def ImageURL(self):
        try:
            url= self.pic.url
        except:
            url=''
        return url


class AmenitiesList(models.Model):
    room = models.ForeignKey(RoomOverView,on_delete=models.CASCADE)
    amenities = models.ForeignKey(Amenities,on_delete=models.CASCADE)

class Offer(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=20,decimal_places=2)
    from_date = models.DateField()
    to_date = models.DateField()
    start = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return date.today() > self.to_date
    
    @property
    def is_started(self):
        return date.today() >= self.from_date

class Coupen(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coupen_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    percent = models.IntegerField()
    start = models.DateField()
    end = models.DateField()
    used = models.BooleanField(default=False)
    live = models.BooleanField(default=False)

    @property
    def is_started(self):
        return date.today() >= self.start


    @property
    def is_valid(self):
        return date.today() > self.end


                 

    