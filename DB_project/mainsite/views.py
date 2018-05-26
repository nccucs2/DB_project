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
from mainsite.models import student_info
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
            # create alphabet for 1st char of ID
            alphabet = list(string.ascii_uppercase[0:8])
            alphabet.extend(list(string.ascii_uppercase[9:]))
            code = list(range(10,33))
            # create the location mapping code for char of ID
            locationCode = dict(zip(alphabet,code))
            id = password
            if len(id) != 10 or not(id[0].isalpha()) \
                or (int[id[1] > 2 or id[1] < 1]):
                user = None
                #print('Error: wrong format')
                # Convert 1st Alphabet to Numeric code
            else:
                encodeID = list(str(locationCode[id[0].upper()]))
                encodeID.extend(list(id[1:]))
                print(encodeID)
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
                if checkSum % 10 == 0:
                    # print("ID is correct")
                    User.objects.create_user(username=password, password=password)
                    user = auth.authenticate(username=password, password=password)
                else:
                    # print('Error: ID is not correct')
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



        #return render_to_response('login.html')
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return HttpResponseRedirect('/accounts/identify/')
#         else:
#             messages.error(request,'輸入格式有誤!')
#     else:
#         form = UserCreationForm()
#     return render(request,'register.html',{'form':form})
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

def suggest_course(request):
    return render(request,'suggest_course.html')
# Create your views here.
