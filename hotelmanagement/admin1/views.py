from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import auth,User  
from user.models import *
from .models import *
from django.core.files import File
from django.contrib import messages
from django.template import loader, Template
import ast
from django.contrib.auth.hashers import make_password
from datetime import date
from reception.models import *
from django.db.models import Avg, Count, Sum
from datetime import datetime , date, timedelta
import base64
from django.core.files.base import ContentFile

# Create your views here.
def login(request):
    if request.session.has_key('password'):
        return redirect(adminhome)
    else:
        if request.method=='POST':
            adminname = request.POST['adminname']
            password = request.POST['password']
            if(adminname=='admin' and password=='admin'):
                request.session['password']=password
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return render(request,'admin/adminlogin.html')

def adminhome(request):
    if request.session.has_key('password'):
        user = User.objects.all().count()
        book1 = BookRoom.objects.all().count()
        book2 = ReceptionBook.objects.all().count()
        room = RoomOverView.objects.all()
        total = 0
        for x in room:
            total = total + x.rooms
        day = date.today()
        userbook = BookRoom.objects.filter(check_in=day)
        no_room = 0
        for x in userbook:
            if x.block == False:
                no_room += x.no_of_room
        receptionbook = ReceptionBook.objects.filter(check_in=day)
        for x in receptionbook:
            no_room += x.no_of_room
        available = total-no_room
        book = book1+book2
        sales1 = 0
        sales2 = 0
        user_book = BookRoom.objects.all()
        for x in user_book:
            sales1 = sales1 + int(x.price)

        rec_book = ReceptionBook.objects.all()
        for x in rec_book:
            sales2 = sales2 + int(x.price)
        sales = sales1 + sales2
        y01 = datetime.now().year
        y02 = y01-1
        y03 = y02-1
        y04 = y03-1
        y05 = y04-1
        salesy1=0
        salesy2=0
        salesy3=0
        salesy4=0
        salesy5=0
        booky1 = BookRoom.objects.filter(check_in__year=y01)
        booky2 = BookRoom.objects.filter(check_in__year=y02)
        booky3 = BookRoom.objects.filter(check_in__year=y03)
        booky4 = BookRoom.objects.filter(check_in__year=y04)
        booky5 = BookRoom.objects.filter(check_in__year=y05)
        for x in booky1:
            salesy1 = salesy1 + x.price
        for x in booky2:
            salesy2 = salesy2 + x.price
        for x in booky3:
            salesy3 = salesy3 + x.price
        for x in booky4:
            salesy4 = salesy4 + x.price
        for x in booky5:
            salesy5 = salesy5 + x.price
        recbook1 = ReceptionBook.objects.filter(check_in__year=y01)
        recbook2 = ReceptionBook.objects.filter(check_in__year=y02)
        recbook3 = ReceptionBook.objects.filter(check_in__year=y03)
        recbook4 = ReceptionBook.objects.filter(check_in__year=y04)
        recbook5 = ReceptionBook.objects.filter(check_in__year=y05)
        for x in recbook1:
            salesy1 = salesy1 + x.price
        for x in recbook2:
            salesy2 = salesy2 + x.price
        for x in recbook3:
            salesy3 = salesy3 + x.price
        for x in recbook4:
            salesy4 = salesy4 + x.price
        for x in recbook5:
            salesy5 = salesy5 + x.price
        m1 = datetime.now().month
        m2 = m1-1
        m3 = m2-1
        m4 = m3-1
        m5 = m4-1
        salesm1 =0
        salesm2 = 0
        salesm3 = 0
        salesm4 = 0
        salesm5 = 0
        booky1 = BookRoom.objects.filter(check_in__month=m1)
        booky2 = BookRoom.objects.filter(check_in__month=m2)
        booky3 = BookRoom.objects.filter(check_in__month=m3)
        booky4 = BookRoom.objects.filter(check_in__month=m4)
        booky5 = BookRoom.objects.filter(check_in__month=m5)
        for x in booky1:
            salesm1 = salesm1 + x.price
        for x in booky2:
            salesm2 = salesm2 + x.price
        for x in booky3:
            salesm3 = salesm3 + x.price
        for x in booky4:
            salesm4 = salesm4 + x.price
        for x in booky5:
            salesm5 = salesm5 + x.price
        booky1 = ReceptionBook.objects.filter(check_in__month=m1)
        booky2 = ReceptionBook.objects.filter(check_in__month=m2)
        booky3 = ReceptionBook.objects.filter(check_in__month=m3)
        booky4 = ReceptionBook.objects.filter(check_in__month=m4)
        booky5 = ReceptionBook.objects.filter(check_in__month=m5)
        for x in booky1:
            salesm1 = salesm1 + x.price
        for x in booky2:
            salesm2 = salesm2 + x.price
        for x in booky3:
            salesm3 = salesm3 + x.price
        for x in booky4:
            salesm4 = salesm4 + x.price
        for x in booky5:
            salesm5 = salesm5 + x.price
        print(salesm1,salesm2,salesm3,salesm4,salesm5)
        d1 = date.today()
        d2 = d1-timedelta(days=1)
        d3 = d2-timedelta(days=1)
        d4 = d3-timedelta(days=1)
        d5 = d4-timedelta(days=1)
        d6 = d5-timedelta(days=1)
        d7 = d6-timedelta(days=1)
        d8 = d7-timedelta(days=1)
        d9 = d8-timedelta(days=1)
        d10 = d9-timedelta(days=1)
        salesd1=0
        salesd2=0
        salesd3=0
        salesd4=0
        salesd5=0
        salesd6=0
        salesd7=0
        salesd8=0
        salesd9=0
        salesd10=0
        booky1 = BookRoom.objects.filter(check_in=d1)
        booky2 = BookRoom.objects.filter(check_in=d2)
        booky3 = BookRoom.objects.filter(check_in=d3)
        booky4 = BookRoom.objects.filter(check_in=d4)
        booky5 = BookRoom.objects.filter(check_in=d5)
        booky6 = BookRoom.objects.filter(check_in=d6)
        booky7 = BookRoom.objects.filter(check_in=d7)
        booky8 = BookRoom.objects.filter(check_in=d8)
        booky9 = BookRoom.objects.filter(check_in=d9)
        booky10 = BookRoom.objects.filter(check_in=d10)
        for x in booky1:
            salesd1 = salesd1 + x.price
        for x in booky2:
            salesd2 = salesd2 + x.price
        for x in booky3:
            salesd3 = salesd3 + x.price
        for x in booky4:
            salesd4 = salesd4 + x.price
        for x in booky5:
            salesd5 = salesd5 + x.price
        for x in booky6:
            salesd6 = salesd6 + x.price
        for x in booky7:
            salesd7 = salesd7 + x.price
        for x in booky8:
            salesd8 = salesd8 + x.price
        for x in booky9:
            salesd9 = salesd9 + x.price
        for x in booky10: 
            salesd10 = salesd10 + x.price
        booky1 = ReceptionBook.objects.filter(check_in=d1)
        booky2 = ReceptionBook.objects.filter(check_in=d2)
        booky3 = ReceptionBook.objects.filter(check_in=d3)
        booky4 = ReceptionBook.objects.filter(check_in=d4)
        booky5 = ReceptionBook.objects.filter(check_in=d5)
        booky6 = ReceptionBook.objects.filter(check_in=d6)
        booky7 = ReceptionBook.objects.filter(check_in=d7)
        booky8 = ReceptionBook.objects.filter(check_in=d8)
        booky9 = ReceptionBook.objects.filter(check_in=d9)
        booky10 = ReceptionBook.objects.filter(check_in=d10)
        for x in booky1:
            salesd1 = salesd1 + x.price
        for x in booky2:
            salesd2 = salesd2 + x.price
        for x in booky3:
            salesd3 = salesd3 + x.price
        for x in booky4:
            salesd4 = salesd4 + x.price
        for x in booky5:
            salesd5 = salesd5 + x.price
        for x in booky6:
            salesd6 = salesd6 + x.price
        for x in booky7:
            salesd7 = salesd7 + x.price
        for x in booky8:
            salesd8 = salesd8 + x.price
        for x in booky9:
            salesd9 = salesd9 + x.price
        for x in booky10: 
            salesd10 = salesd10 + x.price
        q0 = datetime.today()
        q1 = q0-timedelta(days=60)
        q2 = q1-timedelta(days=60)
        q3 = q2-timedelta(days=60)
        q4 = q3-timedelta(days=60)
        q5 = q4-timedelta(days=60)
        q6 = q5-timedelta(days=60)
        q7 = q6-timedelta(days=60)
        q8 = q7-timedelta(days=60)
        q9 = q8-timedelta(days=60)
        sq1 = 0
        sq2 = 0
        sq3 = 0
        sq4 = 0
        sq5 = 0
        sq6 = 0
        sq7 = 0
        sq8 = 0
        sq9 = 0 
        book1 = BookRoom.objects.filter(check_in__range=(q1,q0))
        book2 = BookRoom.objects.filter(check_in__range=(q2,q1))
        book3 = BookRoom.objects.filter(check_in__range=(q3,q2))
        book4 = BookRoom.objects.filter(check_in__range=(q4,q3))
        book5 = BookRoom.objects.filter(check_in__range=(q5,q4))
        book6 = BookRoom.objects.filter(check_in__range=(q6,q5))
        book7 = BookRoom.objects.filter(check_in__range=(q7,q6))
        book8 = BookRoom.objects.filter(check_in__range=(q8,q7))
        book9 = BookRoom.objects.filter(check_in__range=(q9,q8))
        for x in book1:
            sq1 = sq1 + x.price
        for x in book2:
            sq2 = sq2 + x.price
        for x in book3:
            sq3 = sq3 + x.price
        for x in book4:
            sq4 = sq4 + x.price
        for x in book5:
            sq5 = sq5 + x.price
        for x in book6:
            sq6 = sq6 + x.price
        for x in book7:
            sq7 = sq7 + x.price
        for x in book8:
            sq8 = sq8 + x.price
        for x in book9:
            sq9 = sq9 + x.price
        book1 = ReceptionBook.objects.filter(check_in__range=(q1,q0))
        book2 = ReceptionBook.objects.filter(check_in__range=(q2,q1))
        book3 = ReceptionBook.objects.filter(check_in__range=(q3,q2))
        book4 = ReceptionBook.objects.filter(check_in__range=(q4,q3))
        book5 = ReceptionBook.objects.filter(check_in__range=(q5,q4))
        book6 = ReceptionBook.objects.filter(check_in__range=(q6,q5))
        book7 = ReceptionBook.objects.filter(check_in__range=(q7,q6))
        book8 = ReceptionBook.objects.filter(check_in__range=(q8,q7))
        book9 = ReceptionBook.objects.filter(check_in__range=(q9,q8))
        for x in book1:
            sq1 = sq1 + x.price
        for x in book2:
            sq2 = sq2 + x.price
        for x in book3:
            sq3 = sq3 + x.price
        for x in book4:
            sq4 = sq4 + x.price
        for x in book5:
            sq5 = sq5 + x.price
        for x in book6:
            sq6 = sq6 + x.price
        for x in book7:
            sq7 = sq7 + x.price
        for x in book8:
            sq8 = sq8 + x.price
        for x in book9:
            sq9 = sq9 + x.price
        print(sq1,sq2,sq3,sq4,sq5,sq6,sq7,sq8,sq9)
        context = {'count_user':user,'available':available,'total_room':total,'count_book':book,'sales':sales,'y1':salesy1,'y2':salesy2,'y3':salesy3,'y4':salesy4,'y5':salesy5,'year1':y01,'year2':y02,'year3':y03,'year4':y04,'year5':y05,'m1':salesm1,'m2':salesm2,'m3':salesm3,'m4':salesm4,'m5':salesm5,'month1':m1,'month2':m2,'month3':m3,'month4':m4,'month5':m5,
        'd1':salesd1,'d2':salesd2,'d3':salesd3,'d4':salesd4,'d5':salesd5,'d6':salesd6,'d7':salesd7,'d8':salesd8,'d9':salesd9,'d10':salesd10,'date1':d1,'date2':d2,'date3':d3,'date4':d4,'date5':d5,'date6':d6,'date7':d7,'date8':d8,'date9':d9,'date10':d10,'q1':sq1,'q2':sq2,'q3':sq3,'q4':sq4,'q5':sq5,'q6':sq6,'q7':sq7,'q8':sq8,'q9':sq9,
        'Q1':q1,'Q2':q2,'Q3':q3,'Q4':q4,'Q5':q5,'Q6':q6,'Q7':q7,'Q8':q8,'Q9':q9} 
        return render(request,'admin/adminhome.html',context) 
    else:
        return redirect(login)

def logout(request):
    if request.session.has_key('password'):
        request.session.flush()
        return redirect(login) 


def viewuser(request):
    if request.session.has_key('password'):
        users = Details.objects.all() #details model can access User model by calling by user.user
        if request.session.has_key('password'):
            return render(request,'admin/viewuser.html',{'users':users})
        else:
            return redirect(login)
    else:
        return redirect(login)
def edituser(request,id):
    if request.session.has_key('password'):
        if request.method=='POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            if User.objects.filter(username=username).exclude(id=id).exists():
                return JsonResponse('user',safe=False)
            elif User.objects.filter(email=email).exclude(id=id).exists():
                return JsonResponse('email',safe=False)
            else:
                user1 = User.objects.get(id=id)
                user = Details.objects.get(user_id=id)
                user1.first_name = first_name
                user1.last_name = last_name
                user1.username = username
                user1.email = email
                user.phone = phone
                user1.save()
                user.save()
                return JsonResponse('true',safe=False)
        else:
            user = Details.objects.get(user_id=id)
            return render(request,'admin/edituser.html',{'user':user})
    else:
        return redirect(login)
def adduser(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                return JsonResponse('user',safe=False)
            elif User.objects.filter(email=email).exists():
                return JsonResponse('email',safe=False)
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                Details.objects.create(phone=phone,user=user)
                return JsonResponse('true',safe=False)
        else:
            return render(request,'admin/adduser.html')
    else:
        return redirect(login)
def deleteuser(request,id):
    if request.session.has_key('password'):
        user1 = Details.objects.get(user_id=id)
        user = User.objects.get(id=id)
        user1.delete()
        user.delete()
        return redirect(viewuser)
    else:
        return redirect(login)
    

def blockuser(request,id):
    if request.session.has_key('password'):
        user = User.objects.get(id=id)
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect(viewuser)
    else:
        return redirect(login)
def viewreceptionist(request):
    if request.session.has_key('password'):
        reception = Receptionist.objects.all()
        return render(request,'admin/viewreceptionist.html',{'reception':reception})
    else:
        return redirect(login)
def editreceptionist(request,id):
    if request.session.has_key('password'):
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = Receptionist.objects.get(id=id)
            user.username = username
            user.password = password
            user.save()
            return JsonResponse('true',safe=False)
        else:
            user = Receptionist.objects.get(id=id)
            return render(request,'admin/editreceptionist.html',{'user':user})
    else:
        return redirect(login)    
    
def addreceptionist(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            if Receptionist.objects.filter(username=username).exists():
                return JsonResponse('user',safe=False)
            else:
                Receptionist.objects.create(username=username,password=make_password(password))
                return JsonResponse('true',safe=False)
        else:
            return render(request,'admin/addreceptionist.html')
    else:
        return redirect(login)
def deletereceptionist(request,id):
    if request.session.has_key('password'):
        user = Receptionist.objects.get(id=id)
        user.delete()
        return redirect(viewreceptionist)
    else:
        return redirect(login)
def viewrooms(request):
    if request.session.has_key('password'):
        room = RoomOverView.objects.all()
        setamenities = AmenitiesList.objects.all()
        return render(request,'admin/viewrooms.html',{'rooms':room,'setamenities':setamenities})
    else:
        return redirect(login)

def add_over_view(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            rooms = request.POST['room_no']
            price = request.POST['price']
            description = request.POST['description']
            category = request.POST['category']
            category1 = Category.objects.get(id=category)
            amenities = request.POST.getlist('name')
            try:
                room = RoomOverView.objects.create(category=category1,rooms=rooms,available=rooms,description=description,price=price)
                for aminity in amenities:
                    am = Amenities.objects.get(id=aminity)
                    AmenitiesList.objects.create(room=room ,amenities=am)
                return redirect(viewrooms)
            except:
                messages.error(request,'Room already existing, you can edit them!')
                return redirect(add_over_view)
            
        else:
            category = Category.objects.all()
            amenities = Amenities.objects.all()
            context = {'category':category,'amenities':amenities}
            return render(request,'admin/addoverview.html',context)
    else:
        return redirect(login)
def add_room_pic(request,id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            image = request.POST['64input']
            room = RoomOverView.objects.get(id=id)
            room_category = room.category.category
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=room_category + '.' + ext)
            RoomPic.objects.create(room=room, pic=data)
            return redirect(viewrooms)
        else:
            room = RoomOverView.objects.get(id=id)
            context = {'room':room}
            return render(request,'admin/addroompic.html',context)  
    else:
        return redirect(login)
            
def view_room_pic(request,id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            pass
        else:
            room = RoomOverView.objects.get(id=id)
            roompic = RoomPic.objects.filter(room=room)
            context = {'roompics':roompic,'room':room}
            return render(request,'admin/viewroompic.html',context) 
    else:
        return redirect(login)              

def remove_pic(request,id):
    if request.session.has_key('password'):
        roompic = RoomPic.objects.get(id=id)
        roompic.delete()
        return redirect(viewrooms)
    else:
        return redirect(login)


def edit_over_view(request,id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            room = RoomOverView.objects.get(id=id)
            room.rooms=request.POST['room_no']
            room.price = request.POST['price']
            room.description = request.POST['description']
            category0=request.POST['category']
            category = Category.objects.get(id=category0)
            room.category = category
            setamenities = AmenitiesList.objects.filter(room=room)
            setamenities.delete()
            amenities = request.POST.getlist('name')
            for x in amenities:
                amenity = Amenities.objects.get(id=x)
                AmenitiesList.objects.create(room=room,amenities=amenity)
            room.save()
            return redirect(viewrooms)
        else:
            amenities = Amenities.objects.all()
            setamenities_list=[]
            room = RoomOverView.objects.get(id=id)
            setamenities = AmenitiesList.objects.filter(room=room.id)
            for x in setamenities:
                setamenities_list.append(x.amenities.amenities)
            categories = Category.objects.all()
            contex = {'room':room, 'categories':categories, 'setamenities_list':setamenities_list,'amenities':amenities}
            return render(request,'admin/editoverview.html',contex) 
    else:
        return redirect(login)
  
def delete_over_view(request,id):
    if request.session.has_key('password'):
        print(id)
        room = RoomOverView.objects.get(id=id)
        amenities = AmenitiesList.objects.filter(room=room)
        amenities.delete()
        room.delete()
        return redirect(viewrooms)
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
                return render(request,'admin/roomstatus.html',context)
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
                return render(request,'admin/roomstatus.html',context)
    else:
        return redirect(login)

def categories(request):
    if request.session.has_key('password'):
        cate = Category.objects.all()
        return render(request, 'admin/category.html',{'categories':cate})
    else:
        return redirect(login)

def addcategory(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            category_name = request.POST['category']
            if Category.objects.filter(category=category_name).exists():
                messages.error(request,'catogory already exist!')
                return redirect(addcategory)
            else:
                Category.objects.create(category=category_name)
                return redirect(categories)
        else:
            return render(request, 'admin/addcategory.html')
    else:
        return redirect(login)

def deletecategory(request,id):
    if request.session.has_key('password'):
        cate = Category.objects.get(id=id)
        cate.delete()
        return redirect(categories)
    else:
        return redirect(login)
def amenities1(request):
    if request.session.has_key('password'):
        amenity = Amenities.objects.all()
        return render(request,'admin/amenities.html',{'amenities':amenity})
    else:
        return redirect(login)

def addamenities(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            ameneties = request.POST['amenities']
            if Amenities.objects.filter(amenities=ameneties).exists():
                messages.error(request,'amenities already existing!')
                return redirect(addamenities)
            else:
                Amenities.objects.create(amenities=ameneties)
                return redirect(amenities1)
        else:
            return render(request,'admin/addamenities.html')
    else:
        return redirect(login)
def deleteamenities(request,id):
    if request.session.has_key('password'):
        amen = Amenities.objects.get(id=id)
        amen.delete()
        return redirect(amenities1)
    else:
        return redirect(login)
def bookings(request):
    if request.session.has_key('password'):
        book = BookRoom.objects.all()
        contex = {'book':book}
        return render(request,'admin/viewbooking.html',contex)
    else:
        return redirect(login)

def blockbook(request,id):
    if request.session.has_key('password'):
        book = BookRoom.objects.get(id=id)
        if book.block == False:
            book.block = True
            book.save()
        return redirect(bookings)
    else:
        return redirect(login)
def deletebook(request,id):
    if request.session.has_key('password'):
        book = BookRoom.objects.get(id=id)
        if book.block == False:
            room = RoomOverView.objects.get(category = book.room.category)
            room.available = room.available + book.no_of_room
            room.save()
        book.delete()
        return redirect(bookings)
    else:
        return redirect(login)

def reception_book(request):
    if request.session.has_key('password'):
        reception_book = ReceptionBook.objects.all()
        contex = {'receptionbook':reception_book}
        return render(request,'admin/receptionbook.html',contex)
    else:
        return redirect(login)
def editbooking(request):
    pass


def reports(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            from_date = request.POST['from']
            to_date = request.POST['to']
            userbook = BookRoom.objects.filter(check_in__range = (from_date,to_date))
            recbook = ReceptionBook.objects.filter(check_in__range = (from_date,to_date))
            context = {'user_book':userbook, 'reception_book':recbook}
            return render(request,'admin/report.html',context)
        else:
            today = date.today()
            week = date.today() - timedelta(days=7)
            book = BookRoom.objects.filter(check_in__range = (week,today))
            rec_book = ReceptionBook.objects.filter(check_in__range = (week,today))
            return render(request,'admin/report.html',{'user_book':book,'reception_book':rec_book}) 
    else:
        return redirect(login)
def datereport(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            sort = request.POST['sort']
            if sort == 'today':
                today = date.today()
                book = BookRoom.objects.filter(check_in=today)
                rec_book = ReceptionBook.objects.filter(check_in=today)
                return render(request,'admin/report.html',{'user_book':book,'reception_book':rec_book})
            elif sort == 'week':
                today = date.today()
                week = date.today() - timedelta(days=7)
                book = BookRoom.objects.filter(check_in__range = (week,today))
                rec_book = ReceptionBook.objects.filter(check_in__range = (week,today))
                return render(request,'admin/report.html',{'user_book':book,'reception_book':rec_book})
            elif sort == 'month':
                to = date.today()
                from_date = date.today() - timedelta(days=30    )
                book = BookRoom.objects.filter(check_in__range = (from_date,to))
                rec_book = ReceptionBook.objects.filter(check_in__range = (from_date,to))
                return render(request,'admin/report.html',{'user_book':book,'reception_book':rec_book})
            else:
                to = date.today()- timedelta(days=365)
                from_date = to - timedelta(days=365)
                book = BookRoom.objects.filter(check_in__range = (from_date,to))
                rec_book = ReceptionBook.objects.filter(check_in__range = (from_date,to))
                return render(request,'admin/report.html',{'user_book':book,'reception_book':rec_book})
        else:
            return redirect(adminhome)
    else:
        return redirect(login)

def view_reviews(request):
    if request.session.has_key('password'):
        reviews = Review.objects.all()
        return render(request,'admin/viewreview.html',{'reviews':reviews})
    else:
        return redirect(login)

def view_offer(request):
    if request.session.has_key('password'):
        offer = Offer.objects.all()
        if Coupen.objects.exists():
            coupen = Coupen.objects.all()[0]
            context = {'offers':offer,'coupen':coupen,'coupen_exist':True}
        else:
            context = {'offers':offer}
        return render(request,'admin/viewoffer.html',context)
def add_offer(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            offer_name = request.POST['offer_name']
            category0 = request.POST['category']
            discount = request.POST['discount']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            category = Category.objects.get(id=category0)
            if Offer.objects.filter(category=category).exists():
                return JsonResponse('false',safe=False)
            else:
                Offer.objects.create(category=category,offer_name=offer_name,discount=discount,from_date=from_date,to_date=to_date)
                return JsonResponse('true',safe=False)
        else:
            rooms = RoomOverView.objects.all()
            context = {'rooms':rooms}
            return render(request,'admin/addoffer.html',context)
    else:
        return redirect(login)

def delete_offer(request,id):
    if request.session.has_key('password'):
        offer = Offer.objects.get(id=id)
        offer.delete()
        return redirect(view_offer)
    else:
        return redirect(login)

def add_coupen(request):
    if request.session.has_key('password'):
        if request.method=='POST':
            coupen_name = request.POST['coupen_name']
            coupen_code = request.POST['coupen_code']
            percent = request.POST['percent']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            print(coupen_name,coupen_code,percent,from_date,to_date)
            users = User.objects.all()
            for x in users:
                Coupen.objects.create(user=x,code=coupen_code,coupen_name=coupen_name,percent=percent,start=from_date,end=to_date)
            return JsonResponse('true',safe=False)
        else:
            return render(request,'admin/addcoupen.html')
    else:
        return redirect(login)
def delete_coupen(request):
    if request.session.has_key('password'):
        users = User.objects.all()
        for x in users:
            coupen = Coupen.objects.get(user=x)
            coupen.delete()
        return redirect(view_offer)
    else:
        return redirect(login)


