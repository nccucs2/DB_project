from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Passenger(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    # id = models.OneToOneField(User,on_delete=models.CASCADE)


class Train(models.Model):
    train_id = models.CharField(max_length=20)
    num_of_seat = models.SmallIntegerField()

class Run(models.Model):
    run_id = models.CharField(max_length=20)
    start_station = models.CharField(max_length=20)
    dest_station = models.CharField(max_length=20)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    train_id = models.ForeignKey(Train,on_delete=models.CASCADE)

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    run_id = models.ForeignKey(Run,on_delete=models.CASCADE)
    id_phone_num = models.ForeignKey(Passenger,on_delete=models.CASCADE)


class Station(models.Model):
    station_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

class Seat(models.Model):
    train_id = models.ForeignKey(Train,on_delete=models.CASCADE)
    seat_id = models.CharField(max_length=20)

class Pass(models.Model):
    run_id = models.ForeignKey(Run,on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station,on_delete=models.CASCADE)
