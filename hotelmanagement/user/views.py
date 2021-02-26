from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import *
from django.http import JsonResponse
from admin1.models import *
from reception.models import *
from django.contrib import messages
import random
import requests
import json
from django.core.files import File
# Create your views here.
def home(request):
        book = BookRoom.objects.all()
        for x in book:
            if x.is_past_due == True:
                if x.checked_out == False:
                    room1 = RoomOverView.objects.get(category=x.room.category)
                    room1.available = room1.available + x.no_of_room
                    room1.save()
                    x.checked_out = True
                    x.save()
        reception_book = ReceptionBook.objects.all()
        for x in reception_book:
            if x.is_past_due == True:
                if x.checked_out == False:
                    room1 = RoomOverView.objects.get(category=x.room.category)
                    room1.available = room1.available + x.no_of_room
                    room1.save()
                    x.checked_out = True
                    x.save()
        offer = Offer.objects.all()
        for x in offer:
            if x.is_started==True:
                x.start=True
                x.save()
            if x.is_valid == True:
                x.delete()
        users = User.objects.all()
        for x in users:
            coupen = Coupen.objects.get(user=x)
            if coupen.is_started == True:
                coupen.live = True
                coupen.save()
            if coupen.is_valid==True:
                coupen.delete()

        room = RoomOverView.objects.all()
        category = Category.objects.all()
        amenities = Amenities.objects.all()
        setamenities = AmenitiesList.objects.all()
        contex = {'rooms':room,'categories':category,'amenities':amenities,'setamenities':setamenities}
        return render(request,'user/index.html',contex)
    
def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                details = Details.objects.get(user=user)
                if details.Id_proof=='':
                    print('error')
                    request.session['username']=username
                    return JsonResponse('addid',safe=False)
                else:
                    auth.login(request,user)
                    return JsonResponse('true',safe=False)
                
            else:
                return JsonResponse('false',safe=False)
        else:
            return render (request,'user/userlogin.html')


    


def otp_check(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            if Details.objects.filter(phone=phone).exists():
                request.session['phone'] = phone
                url = "https://d7networks.com/api/verifier/send"
                phone1 = '91'+str(phone)
                payload = {'mobile': phone1,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'} 
                files = [

                ]
                headers = {
                'Authorization': 'Token cbad324544bd072bb68feb55055c0f79085f1bd7'
                }

                response = requests.request("POST", url, headers=headers, data = payload, files = files)
                print(response.text.encode('utf8'))
                data = response.text.encode('utf8')
                dict=json.loads(data.decode('utf8'))
                otp_id = dict["otp_id"]
                request.session['otp_id']=otp_id
                print(request.session['otp_id'])
                
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
                
        else:
            return render(request,'user/otp.html')

def varification(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            phone = request.session['phone']
            url = "https://d7networks.com/api/verifier/verify"
            otp = request.POST['otp']
            user = Details.objects.get(phone=phone)
            otp_id = request.session['otp_id']
            print(otp_id)
            payload = {'otp_id': otp_id ,
            'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token cbad324544bd072bb68feb55055c0f79085f1bd7'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            
            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            status=dict['status']
            if status == 'success':
                auth.login(request,user)
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            if request.session.has_key('otp_id'):
                phone = request.session['phone']
                context = {'phone':phone}
                return render(request,'user/varification.html',context)
            else:
                return redirect(otp_check)
                


def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(email=email).exists() :
                return JsonResponse('email',safe=False)
            elif User.objects.filter(username=username).exists() :
                return JsonResponse('user',safe=False)
            elif Details.objects.filter(phone=phone).exists():
                return JsonResponse('phone',safe=False)
            else:
                user= User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                Details.objects.create(phone = phone,user = user)
                return JsonResponse('true',safe=False)
        else:
            return render(request, 'user/signup.html')

def add_id_proof(request):
    if request.user.is_authenticated:
        pass
    else:
        if request.method=='POST':
            username = request.session['username']
            user = User.objects.get(username=username)
            details = Details.objects.get(user=user)
            id_proof = request.FILES.get('id_pic')
            print(id_proof)
            details.Id_proof=id_proof
            details.save()
            auth.login(request,user)
            return redirect(home)
        else:
            username = request.session['username']
            user = User.objects.get(username=username)
            return render(request,'user/addid.html',{'user':user})

def specific_room(request,id):
    if request.method=='POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        no_of_room = int(request.POST['no_of_room'])
        no_of_guest = request.POST['no_of_guest']
        price = request.POST['price']
        method = request.POST['method']
        user = request.user
        room = RoomOverView.objects.get(id=id)
        if room.available>no_of_room:
            if method=='cod':
                room.available = room.available-no_of_room
                room.save()
                BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=False,checked_out=False,price=price)
                return JsonResponse('true',safe=False)
            elif method=='paypal':
                room.available -= no_of_room
                room.save()
                BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                return JsonResponse('true',safe=False)
            elif method=='razorpay':
                room.available -= no_of_room
                room.save()
                BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                return JsonResponse('true',safe=False)
            else:
                coupen = Coupen.objects.get(user=user)
                coupen.used = False
                coupen.save()
                return JsonResponse('false',safe=False)
        else:
            coupen = Coupen.objects.get(user=user)
            coupen.used = False
            coupen.save()
            return JsonResponse('room',safe=False)
    else:
        if request.user.is_authenticated:
            room = RoomOverView.objects.get(id=id)
            setamenities = AmenitiesList.objects.filter(room=room.id)
            total = int(room.price/70)
            reviews = Review.objects.filter(category=room.category)
            user = request.user
            if Coupen.objects.filter(user=user).exists():
                coupen = Coupen.objects.get(user=user)
                if Offer.objects.filter(category=room.category).exists():
                    offer = Offer.objects.get(category=room.category)
                    if offer.start==True:
                        start = True
                        contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews,'offer':offer,'start':start,'coupen':coupen,'coupen_exist':True}
                        return render(request,'user/viewspecificroom.html',contex)
                else:
                    contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews,'coupen':coupen,'coupen_exist':True}
                    return render(request,'user/viewspecificroom.html',contex)
            else:
                contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews}
                return render(request,'user/viewspecificroom.html',contex)

            
        else:
            return redirect(login)

def view_coupen(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        else:
            user = request.user
            coupen = Coupen.objects.get(user=user)
            context = {'coupen':coupen}
            return render(request,'user/viewcoupen.html',context)
    else:
        return redirect(home)

def check_coupen(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            check_code = request.POST['check_code']
            user = request.user
            coupen = Coupen.objects.get(user=user)
            print(check_code)
            if coupen.used == False:
                if coupen.code == check_code:
                    coupen.used = True
                    coupen.save()
                    return JsonResponse('true',safe=False) 
                else:
                    return JsonResponse('false',safe=False)
            else:
                return JsonResponse('used',safe=False)
        else:
            return redirect(home)
    else:
        return redirect(home)
            

def history(request):
    if request.user.is_authenticated:
        user = request.user
        book = BookRoom.objects.filter(user=user)
        return render(request,'user/history.html', {'booking':book})
    else:
        return redirect(home)


def add_review(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if Review.objects.filter(book=id).exists():   
                print('already exist')
                return JsonResponse('exist',safe=False)
            else:
                book = BookRoom.objects.get(id=id)
                text = request.POST['text']
                category = book.room.category
                Review.objects.create(book=book,review=text,category=category)
                return JsonResponse('true',safe=False)
        else:
            book = BookRoom.objects.get(id=id) 
            context = {'book':book}
            return render(request,'user/addreview.html',context)
    else:
        return redirect(home)

def filter(request):
    category = Category.objects.all()
    amenities = Amenities.objects.all()
    setamenities = AmenitiesList.objects.all()
    if request.method == 'POST':
        amenity_list = []
        categoryf = request.POST['category']
        amenity_listf = request.POST.getlist('amenities[]')
        roomf = int(request.POST['room'])
        room = RoomOverView.objects.get(category=categoryf)
        for x in setamenities:
            if x.room == room:
                amenity_list.append(x.amenities.amenities)
        print(amenity_list)
        print(amenity_listf)
        print(type(room.available))
        print(type(roomf))
        if amenity_listf in amenity_list or room.available >= roomf:
            print('success')
            request.session['room_category'] = categoryf
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        if request.session.has_key('room_category'):
            category1 = request.session['room_category']
            category = Category.objects.get(id = category1)
            room = RoomOverView.objects.get(category=category1)
            context = {'room':room,'category':category,'amenities':amenities,'setamenities':setamenities}
            return render(request, 'user/filter.html', context)
        else:
            return redirect('/')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)

def crop(request):
    
    return render(requests,'crop.html')

        