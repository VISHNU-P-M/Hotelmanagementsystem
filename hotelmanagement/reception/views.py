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
            return render(request,'reception/receptionlogin.html')
def receptionhome(request):
    if request.session.has_key('password'):
        room = RoomOverView.objects.all()
        category = Category.objects.all()
        amenities = Amenities.objects.all()
        setamenities = AmenitiesList.objects.all()
        roompic = RoomPic.objects.all()
        contex = {'rooms':room,'categories':category,'amenities':amenities,'setamenities':setamenities,'roompics':roompic}
        return render(request,'reception/receptionhome.html',contex)
    else:
        return redirect(login)

def roomstatus(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            day = request.POST['date']
            request.session['day'] = day
            return redirect(roomstatus)
        else:
            room = RoomOverView.objects.all()
            if request.session.has_key('day'):
                day = request.session['day']
                del request.session['day']
                avalailable_dict = {}
                for y in room:
                    no_room = 0
                    userbook = BookRoom.objects.filter(check_in=day,room=y)
                    for x in userbook:
                        if x.block == False:
                            no_room += x.no_of_room
                    receptionbook = ReceptionBook.objects.filter(check_in=day,room=y)
                    for x in receptionbook:
                        no_room += x.no_of_room
                    availabe_room = y.rooms - no_room
                    avalailable_dict[y.category.category]=availabe_room
                category = Category.objects.all()
                context = {'rooms':room,'categories':category,'date':day,'available_rooms':avalailable_dict}
                return render(request,'reception/roomstatus.html',context)
            else:
                day = date.today()
                avalailable_dict = {}
                for y in room:
                    no_room = 0
                    userbook = BookRoom.objects.filter(check_in=day,room=y)
                    for x in userbook:
                        if x.block == False:
                            no_room += x.no_of_room
                    receptionbook = ReceptionBook.objects.filter(check_in=day,room=y)
                    for x in receptionbook:
                        no_room += x.no_of_room
                    availabe_room = y.rooms - no_room
                    avalailable_dict[y.category.category]=availabe_room
                category = Category.objects.all()
                context = {'rooms':room,'categories':category,'date':day,'available_rooms':avalailable_dict}
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
            room = RoomOverView.objects.get(id=id)
            userbook = BookRoom.objects.filter(check_in=check_in,room=room)
            no_room = 0
            for x in userbook:
                if x.block == False:
                    no_room += x.no_of_room
            receptionbook = ReceptionBook.objects.filter(check_in=check_in, room=room)
            for x in receptionbook:
                no_room += x.no_of_room
            availabe_room = room.rooms - no_room
            if availabe_room>=no_of_room:
                room.available = room.available - no_of_room
                room.save()
                ReceptionBook.objects.create(reception=receptionist, room=room ,guest_name=guest_name,contact=phone,check_out=check_out,check_in=check_in,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            room = RoomOverView.objects.get(id=id)
            roompics = RoomPic.objects.filter(room=room)
            setamenities = AmenitiesList.objects.filter(room=room.id)
            return render(request,'reception/receptionspecificroom.html',{'rooms':room,'amenities':setamenities,'roompics':roompics})
    else:
        return redirect(login)

def filter(request):
    category = Category.objects.all()
    amenities = Amenities.objects.all()
    setamenities = AmenitiesList.objects.all()
    if request.method == 'POST':
        amenity_list = []
        categoryf = request.POST['category']
        check_in = request.POST['check_in']
        amenity_listf = request.POST.getlist('amenities[]')
        roomf = int(request.POST['room'])
        room = RoomOverView.objects.get(category=categoryf)
        userbook = BookRoom.objects.filter(check_in=check_in,room=room)
        no_room = 0
        for x in userbook:
            if x.block == False:
                no_room += x.no_of_room
        receptionbook = ReceptionBook.objects.filter(check_in=check_in,room=room)
        for x in receptionbook:
            no_room += x.no_of_room
        availabe_room = room.rooms - no_room
        print(availabe_room)
        for x in setamenities:
            if x.room == room:
                amenity_list.append(x.amenities.amenities)
        for x in amenity_listf:
            if x in amenity_list:
                flag = True
            else:
                flag = False
        if availabe_room>=roomf:
            if flag==True:
                print('success')
                request.session['room_category'] = categoryf
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('amenity',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        if request.session.has_key('room_category'):
            category1 = request.session['room_category']
            category = Category.objects.get(id = category1)
            room = RoomOverView.objects.get(category=category1)
            roompic = RoomPic.objects.filter(room=room)
            context = {'room':room,'category':category,'amenities':amenities,'setamenities':setamenities,'roompics':roompic}
            return render(request, 'reception/filter.html', context)
        else:
            return redirect('/reception/')

def logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(login)