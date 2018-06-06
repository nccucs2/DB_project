from django.contrib import admin
from .models import Passenger,Train,Run,Ticket,Station,Seat,Pass
# Register your models here.


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name','phone_number')
admin.site.register(Passenger,PassengerAdmin)

class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_id','num_of_seat')
admin.site.register(Train,TrainAdmin)

class RunAdmin(admin.ModelAdmin):
    list_display = ('run_id','start_station','dest_station','date','time','train_id')
admin.site.register(Run,RunAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display =('ticket_id','name','run_id','id_phone_num')
admin.site.register(Ticket,TicketAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id','name')
admin.site.register(Station,StationAdmin)

class SeatAdmin(admin.ModelAdmin):
    list_display = ('train_id','seat_id')
admin.site.register(Seat,SeatAdmin)

class PassAdmin(admin.ModelAdmin):
    list_display = ('run_id','station_id')
admin.site.register(Pass,PassAdmin)
