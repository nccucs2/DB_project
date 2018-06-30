from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Passenger(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)

    # id = models.OneToOneField(User,on_delete=models.CASCADE)


class Train(models.Model):
    train_id = models.CharField(max_length=20)
    num_of_seat = models.SmallIntegerField()
    def __str__(self):
        return str(self.train_id)


class Run(models.Model):
    run_id = models.CharField(max_length=20)
    start_station = models.CharField(max_length=20)
    dest_station = models.CharField(max_length=20)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    train_id = models.ForeignKey(Train,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.run_id)

class Seat(models.Model):
    train_id = models.ForeignKey(Train,on_delete=models.CASCADE,blank = True,null=True)
    # run_id = models.ForeignKey(Run,on_delete=models.CASCADE,blank = True,null=True)
    seat_id = models.CharField(max_length=20)
    booked = models.BooleanField(default=True)
    def __str__(self):
        return str(self.seat_id)

class Ticket(models.Model):
    passenger = models.ForeignKey(Seat,on_delete=models.CASCADE,default='')
    run_id = models.ForeignKey(Run,on_delete=models.CASCADE)
    id_phone_num = models.ForeignKey(Passenger,on_delete=models.CASCADE,blank = True,null=True)

    def __str__(self):
        return str(self.run_id) + " " + str(self.passenger)



class Station(models.Model):
    station_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)





class Pass(models.Model):
    run_id = models.ForeignKey(Run,on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station,on_delete=models.CASCADE)





"""data input for Run"""
all_obj = []
for e in Train.objects.all():
    all_obj.append(e)

# Run.objects.bulk_create([
# Run(run_id='203',start_station='南港',dest_station='左營',date='2018-06-30',time='10:00',train_id=all_obj[1]),
# Run(run_id='805',start_station='南港',dest_station='台中',date='2018-06-25',time='11:00',train_id=all_obj[2]),
# Run(run_id='1607',start_station='台北',dest_station='左營',date='2018-06-28',time='13:00',train_id=all_obj[3]),
# Run(run_id='805',start_station='南港',dest_station='台中',date='2018-06-25',time='11:00',train_id=all_obj[4]),
# Run(run_id='109',start_station='台北',dest_station='台中',date='2018-06-27',time='23:00',train_id=all_obj[5]),
# Run(run_id='1505',start_station='南港',dest_station='左營',date='2018-06-25',time='13:00',train_id=all_obj[6]),
# Run(run_id='609',start_station='台北',dest_station='左營',date='2018-06-25',time='14:00',train_id=all_obj[7]),
# Run(run_id='205',start_station='南港',dest_station='左營',date='2018-06-24',time='10:00',train_id=all_obj[8]),
# Run(run_id='809',start_station='南港',dest_station='左營',date='2018-06-28',time='14:00',train_id=all_obj[9]),
# Run(run_id='117',start_station='南港',dest_station='左營',date='2018-06-23',time='17:00',train_id=all_obj[10]),
# Run(run_id='567',start_station='台北',dest_station='左營',date='2018-06-28',time='12:00',train_id=all_obj[11]),
# ]
# )
# """data input for Pass"""
# run_obj = []
# for run in Run.objects.all():
#     run_obj.append(run)
#
# station_obj = []
# for station in Station.objects.all():
#     station_obj.append(station)
#
# counter = 0
# station_list ={'左營':0,'台南':1,'嘉義':2,'雲林':3,'彰化':4,'台中':5,'苗栗':6,'新竹':7,'桃園':8,'板橋':9,'台北':10,'南港':11}
#
#
# for run in (run_obj):
#
#     print(run.run_id)
#     if station_list[run.start_station]>station_list[run.dest_station]:
#         for i in range(station_list[run.dest_station],station_list[run.start_station]):
#             print(i)
#             Pass.objects.create(run_id=run,station_id=station_obj[i])
#
#     else:
#         for i in range(station_list[run.start_station],station_list[run.dest_station]):
#             print(i)
#             Pass.objects.create(run_id=run,station_id=station_obj[i])


"""data for seat"""

seat_number=['A','B','C','D','E']
# ticket_list =[12][5]
w, h = 5,12 ;
ticket_list = [[0 for x in range(w)] for y in range(h)]

for i in range(12):
    for j in range(5):
        ticket_list[i][j]=str(i+1)+seat_number[j]

# print(ticket_list)

counter = 0
train_obj = []
for train in Train.objects.all():
    train_obj.append(train)
    # print(counter)
    counter+=1
# print(train_obj)

# for train in train_obj:
#     if train.num_of_seat==500:
#         print(train.train_id)
#         for k in range(10):
#             for i in range(10):
#                 for j in range(5):
#                     Seat.objects.create(train_id=train,seat_id=str(k+1)+'-'+ticket_list[i][j])
#                     print(str(k+1)+'-'+ticket_list[i][j])
#
#     elif train.num_of_seat==600:
#         print(train.train_id)
#         for k in range(12):
#             for i in range(10):
#                 for j in range(5):
#                     Seat.objects.create(train_id=train,seat_id=str(k+1)+'-'+ticket_list[i][j])
#                     print(str(k+1)+'-'+ticket_list[i][j])
