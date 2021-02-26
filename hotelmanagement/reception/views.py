from django.shortcuts import render,redirect
from admin1.models import Receptionist
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from admin1.models import *
from user.models import *
from .models import *

# Create your views here.
def login(request):
    if request.session.has_key('password'):
        return redirect(receptionhome)
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = Receptionist.objects.filter(username=username).first()
            if user is not None and check_password(password,user.password):
                request.session['password']=password
                request.session['username']=username
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return render(request,'receptionlogin.html')
def receptionhome(request):
    if request.session.has_key('password'):
        room = RoomOverView.objects.all()
        category = Category.objects.all()
        amenities = Amenities.objects.all()
        setamenities = AmenitiesList.objects.all()
        contex = {'rooms':room,'categories':category,'amenities':amenities,'setamenities':setamenities}
        return render(request,'reception/receptionhome.html',contex)
    else:
        return redirect(login)

def roomstatus(request):
    if request.session.has_key('password'):
        room = RoomOverView.objects.all()
        category = Category.objects.all()
        context = {'rooms':room,'categories':category}
        return render(request,'reception/roomstatus.html',context)
    else:
        return redirect(login)
def specific_room(request,id):
    if request.session.has_key('password'):
        if request.method=='POST':
            print(request.session['username'])
            username = request.session['username']
            receptionist = Receptionist.objects.get(username=username)
            guest_name = request.POST['guest_name']
            phone = request.POST['phone']
            check_in = request.POST['check_in']
            check_out = request.POST['check_out']
            no_of_room = int(request.POST['no_of_room'])
            no_of_guest = request.POST['no_of_guest']
            price = request.POST['price']
            print(guest_name,phone,check_in,check_out,no_of_guest,no_of_room,price)
            room = RoomOverView.objects.get(id=id)
            if room.available>no_of_room:
                room.available = room.available - no_of_room
                room.save()
                ReceptionBook.objects.create(reception=receptionist, room=room ,guest_name=guest_name,contact=phone,check_out=check_out,check_in=check_in,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            room = RoomOverView.objects.get(id=id)
            setamenities = AmenitiesList.objects.filter(room=room.id)
            return render(request,'reception/receptionspecificroom.html',{'rooms':room,'amenities':setamenities})
    else:
        return redirect(login)

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
            return render(request, 'reception/filter.html', context)
        else:
            return redirect('/reception/')

def logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(login)