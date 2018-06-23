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
# from mainsite.models import student_info
import string
def login(request):
    #template = get_template('login.html')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/student/')
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
            return HttpResponseRedirect('/student/')
    else:
        if request.POST:
            messages.error(request,'查無此身份')
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')
def identify(request):
    if request.POST:
        p=student_info.objects.create(major=request.POST['major'],name=request.POST['name'],number=request.POST['number'])
        p.save();
        return HttpResponseRedirect('/login/')
    return render(request,'identify.html')
def student(request):
    if request.user.is_authenticated:
        return render(request,'student.html')
    else:
        return HttpResponseRedirect('/login/')

def course(request):
    return render(request,'course.html')

def train_query(request):
    station = Station.objects.all()
    return render(request,'train_query.html',{'station':station})


# Create your views here.
