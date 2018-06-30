from django.shortcuts import render,render_to_response
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mainsite.models import Passenger,Train,Run,Ticket,Station,Seat,Pass
import random
# from mainsite.models import student_info
import string
def login(request):
    #template = get_template('login.html')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/menu/')
    try:

        password = request.POST['usr_pass']
        phone_number = request.POST['usr_phone']
        # print(phone_number)


        user = auth.authenticate(username=password, password=password)
        if user is not None:
            try:
                old_phone = Passenger.objects.get(name=user)
                if old_phone.phone_number!=phone_number:
                    old_phone.phone_number=phone_number
                    old_phone.save()
            except:
                Passenger.objects.create(name=user,phone_number=phone_number)


        elif user is None:

            code = [10,11,12,13,14,15,16,17,34,18,19,20,21,22,35,23,24,25,26,27,28,29,32,30,31,33]
            alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

                # create the location mapping code for char of ID
            locationCode = dict(zip(alphabet,code))

            id = password

            if id[0].islower() or len(id) != 10 or not(id[0].isalpha()) \
            or not(id[1:].isdigit()or(int[id[1] > 2 or id[1] < 1])):

                user = None
                    # Convert 1st Alphabet to Numeric code
            else:
                print(id)
                encodeID = list(str(locationCode[id[0].upper()]))
                print(encodeID)
                encodeID.extend(list(id[1:]))
                checkSum = int(encodeID[0])

                        # Calculate the checksum of ID

                para = 9
                for n in encodeID[1:]:
                    if para == 0:
                        para = 1
                    print(n, para)
                    checkSum += int(n)*para
                    para -= 1

                    # Check the checksum
                    # print(id)
                if checkSum % 10 == 0:
                    print("ID is correct")

                    User.objects.create_user(username=password, password=password)
                    user = auth.authenticate(username=password, password=password)
                else:
                    print('Error: ID is not correct')

                    user=None


    except:
        user = None
        phone_number = None

    if (user is not None) and (phone_number is not None):
        print(phone_number)
        if user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('/menu/')
    else:
        if request.POST:
            messages.error(request,'查無此身份')
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def menu(request):
    if request.user.is_authenticated:
        return render(request,'menu.html')
    else:
        return HttpResponseRedirect('/login/')

def do(request):
    if request.POST:
        print(request.POST['id'])
        train=Run.objects.get(run_id=request.POST['id'])
        seat=Seat.objects.filter(train_id=train.train_id,booked=True)
        random_num=random.randint(0,len(seat))
        Ticket.objects.create(passenger=seat[random_num],run_id=Run.objects.get(run_id=request.POST['id']),id_phone_num=Passenger.objects.get(name=request.user))
        seat[random_num].booked=False
        seat[random_num].save()
    return HttpResponseRedirect('/menu/train_query/')

def train_query(request):
    if request.POST:
        start = request.POST['start']
        finish = request.POST['finish']
        time = request.POST['time']
        date = request.POST['date']
        p = Run.objects.all()
        if start != '--':
            p = p.filter(start_station=start)
        if finish != '--':
            p = p.filter(dest_station=finish)
        if time != '--':
            p = p.filter(time=time)
        if date != '--':
            p = p.filter(date=date)
        for i in p :
            print(i)
            # return render(request,'train_run.html',{'runs':p})
            train_run = "車號"
            train_start="起點"
            train_dest="終點"
            train_date="日期"
            train_time="時間"
            return render(request,'train_run.html',{'runs':p},locals())
    station = Station.objects.all()
    return render(request,'train_query.html',{'station':station})

def query_ticket(request):
    info_list=[]
    try:
        q = Ticket.objects.all()
        q = q.filter(id_phone_num__name=request.user)
    except:
        info_list=[]
    return render(request,'query_ticket.html',{'info':q})

def delete_ticket(request):
    ticket = Ticket.objects.get(id=request.POST['id'])
    p=Seat.objects.get(id=ticket.passenger.id)
    p.booked=True
    p.save()
    print(p.booked)
    ticket.delete()
    return HttpResponseRedirect('/menu/query_ticket/')

def modify_ticket(request):
    ticket = Ticket.objects.get(id=request.POST['original_id'])
    ticket.delete()

    train=Run.objects.get(run_id=request.POST['id'])
    seat=Seat.objects.filter(train_id=train.train_id,booked=True)
    random_num=random.randint(0,len(seat))
    Ticket.objects.create(passenger=seat[random_num],run_id=Run.objects.get(run_id=request.POST['id']),id_phone_num=Passenger.objects.get(name=request.user))
    seat[random_num].booked=False
    seat[random_num].save()

    return render(request,'modify_ticket.html',{'myticket':myticket})
# Create your views here.
