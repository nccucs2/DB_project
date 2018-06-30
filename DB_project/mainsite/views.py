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
        # username = request.POST['usr_id']

        password = request.POST['usr_pass']
        user = auth.authenticate(username=password, password=password)

        if user is None:

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


    if user is not None:
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
        return render(request,'train_run.html',{'runs':p})

    station = Station.objects.all()
    return render(request,'train_query.html',{'station':station})

def new_ticket(request):
    print(request.user)
    if request.POST:
        try:
            a = Passenger.objects.get(name=request.user)
            if a.phone_number!=request.POST['phone_number']:
                a.phone_number=request.POST['phone_number']
                a.save()
        except:
            Passenger.objects.create(name=request.user,phone_number=request.POST['phone_number'])
        train=Run.objects.get(run_id=request.POST['train_id'])
        seat=Seat.objects.filter(train_id=train.train_id,booked=True)
        random_num=random.randint(0,len(seat))
        Ticket.objects.create(passenger=seat[random_num],name=request.POST['username'],run_id=Run.objects.get(run_id=request.POST['train_id']),id_phone_num=Passenger.objects.get(name=request.user))
        seat[random_num].booked=False
        seat[random_num].save()
    runs = Run.objects.all()
    return render(request,'new_ticket.html',{'runs':runs})

def query_ticket(request):
    return render(request,'query_ticket.html')

def modify_ticket(request):
    myticket = Ticket.objects.filter(id_phone_num__name=request.user)
    return render(request,'modify_ticket.html',{'myticket':myticket})
# Create your views here.
