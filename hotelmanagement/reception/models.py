from django.db import models
from admin1.models import RoomOverView, Receptionist
from datetime import date
# Create your models here.

class ReceptionBook(models.Model):
    reception = models.ForeignKey(Receptionist, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomOverView, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=50)
    contact = models.BigIntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    no_of_room = models.IntegerField(null=True)
    no_of_guest = models.IntegerField(null=True)
    pay_status = models.BooleanField(null=True)
    checked_out = models.BooleanField(null=True,default=False)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True)


    @property
    def is_past_due(self):
        return date.today() > self.check_out