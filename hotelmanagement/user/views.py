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
from datetime import date,datetime,timedelta
# Create your views here.
def home(request):
    if Offer.objects.exists():
        offer = Offer.objects.all()
        for x in offer:
            if x.is_started==True:
                x.start=True
                x.save()
            if x.is_valid == True:
                x.start=False
                x.save()
    room = RoomOverView.objects.all()
    category = Category.objects.all()
    amenities = Amenities.objects.all()
    setamenities = AmenitiesList.objects.all()
    offer = Offer.objects.all()
    roompics = RoomPic.objects.all()
    contex = {'rooms':room,'categories':category,'amenities':amenities,'setamenities':setamenities,'offers':offer,'roompics':roompics}
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
                    request.session['username']=username
                    return JsonResponse('addid',safe=False)
                else:
                    auth.login(request,user)
                    return JsonResponse('true',safe=False)
                
            else:
                return JsonResponse('false',safe=False)
        else:
            return render (request,'user/userlogin.html')


    
#send otp to Phone no.

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
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
                
        else:
            return render(request,'user/otp.html')

#varifie the otp

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
            del request.session['otp_id']
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
            if details.ImageURL=='':
                messages.error(request,"can't log-in without adding id proof")
                return redirect(add_id_proof)
            else:
                auth.login(request,user)
                return redirect(home)
        else:
            username = request.session['username']
            user = User.objects.get(username=username)
            return render(request,'user/addid.html',{'user':user})

def specific_room(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            check_in_str = request.POST['check_in']
            check_out_str = request.POST['check_out']
            no_of_room = int(request.POST['no_of_room'])
            no_of_guest = request.POST['no_of_guest']
            user = request.user
            room = RoomOverView.objects.get(id=id)
            if room.available >= no_of_room:
                request.session['check_in']=check_in_str
                request.session['check_out']=check_out_str
                request.session['no_of_room']=no_of_room
                request.session['no_of_guest']=no_of_guest
                request.session['room_id']=room.id
                check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
                check_out = datetime.strptime(check_out_str,"%Y-%m-%d").date()
                day = (check_out - check_in).days
                if Offer.objects.filter(category=room.category):
                    offer = Offer.objects.get(category=room.category)
                    if offer.start == True:
                        price0 = offer.discount*day*no_of_room
                        price = float(price0)
                        request.session['price']=price
                        return JsonResponse('true', safe=False)
                    else:
                        price0 = room.price*day*no_of_room
                        price = float(price0)
                        request.session['price']=price
                        return JsonResponse('true',safe=False)
                else:
                    price0 = room.price*day*no_of_room
                    price = float(price0)
                    request.session['price']=price
                    return JsonResponse('true',safe=False)
            else:
                return JsonResponse('room',safe=False)
                pass
        else:
            room = RoomOverView.objects.get(id=id)
            setamenities = AmenitiesList.objects.filter(room=room.id)
            total = int(room.price/70)
            reviews = Review.objects.filter(category=room.category)
            user = request.user
            roompics = RoomPic.objects.filter(room=room)
            if Offer.objects.filter(category=room.category).exists():
                offer = Offer.objects.get(category=room.category)
                if offer.start==True:
                    contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews,'offer':offer,'start':True,'roompics':roompics}
                    return render(request,'user/viewspecificroom.html',contex)
                else:
                    contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews,'roompics':roompics}
                    return render(request,'user/viewspecificroom.html',contex)
            else:
                contex = {'rooms':room,'amenities':setamenities, 'total':total,'reviews':reviews,'roompics':roompics}
                return render(request,'user/viewspecificroom.html',contex)
    else:
        return redirect(home)  

def book_room(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            check_in = request.session['check_in']
            check_out = request.session['check_out']
            no_of_room = request.session['no_of_room']
            no_of_guest = request.session['no_of_guest']
            price = request.POST['price']
            method = request.POST['method']
            id = request.POST['room_id']
            room = RoomOverView.objects.get(id=id)
            user = request.user
            userbook = BookRoom.objects.filter(room=room,check_in=check_in)
            receptionbook = ReceptionBook.objects.filter(room=room,check_in=check_in)
            rooms = 0
            for x in userbook:
                if x.block == False:
                    rooms += x.no_of_room
            for x in receptionbook:
                rooms += x.no_of_room
            availabe_room = room.rooms - rooms
            if no_of_room <= availabe_room:
                if method=='cod':
                    BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=False,checked_out=False,price=price)
                    del request.session['check_in'] 
                    del request.session['check_out']
                    del request.session['no_of_room']
                    del request.session['no_of_guest']
                    del request.session['room_id']
                    del request.session['price']
                    return JsonResponse('true',safe=False)
                elif method=='paypal':
                    BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                    del request.session['check_in']
                    del request.session['check_out']
                    del request.session['no_of_room']
                    del request.session['no_of_guest']
                    del request.session['room_id']
                    del request.session['price']
                    return JsonResponse('true',safe=False)
                elif method=='razorpay':
                    BookRoom.objects.create(user=user,room=room,check_in=check_in,check_out=check_out,no_of_room=no_of_room,no_of_guest=no_of_guest,pay_status=True,checked_out=False,price=price)
                    del request.session['check_in']
                    del request.session['check_out']
                    del request.session['no_of_room']
                    del request.session['no_of_guest']
                    del request.session['room_id']
                    del request.session['price']
                    return JsonResponse('true',safe=False)
                else:
                    coupen = Coupen.objects.get(user=user)
                    coupen.used = False
                    coupen.save()
                    del request.session['check_in']
                    del request.session['check_out']
                    del request.session['no_of_room']
                    del request.session['no_of_guest']
                    del request.session['room_id']
                    del request.session['price']
                    return JsonResponse('false',safe=False)
            else:
                coupen = Coupen.objects.get(user=user)
                coupen.used = False
                coupen.save()
                del request.session['check_in']
                del request.session['check_out']
                del request.session['no_of_room']
                del request.session['no_of_guest']
                del request.session['room_id']
                del request.session['price']
                return JsonResponse('room',safe=False)
        
        else:
            if request.session.has_key('check_in'):
                check_in = request.session['check_in']
                check_out = request.session['check_out']
                no_of_room = request.session['no_of_room']
                no_of_guest = request.session['no_of_guest']
                id = request.session['room_id']
                room = RoomOverView.objects.get(id=id)
                price = request.session['price']
                paypal_price=price/70
                razorpay_price = price*100
                user = request.user
                room_no = []
                number = random.randint(100,200)
                room_no.append(number)
                for i in range(1,no_of_room):
                    number += 1
                    print(number) 
                    room_no.append(number)
                if Coupen.objects.filter(user=user).exists():
                    if request.session.has_key('coupon'):
                        code = request.session['coupon']
                        coupon = Coupen.objects.get(code=code,user=user)
                        discount = int(coupon.percent)
                        discount_price = price - (price*(discount/100))
                        paypal_price = discount_price/70
                        razorpay_price = discount_price*100
                        del request.session['coupon']
                        context = {'check_in':check_in,'check_out':check_out,'room':room,'room_no':room_no,'price':discount_price,'paypal_price':paypal_price,'razorpay_price':razorpay_price}
                        return render(request,'user/book.html',context)
                    else:
                        coupon = Coupen.objects.filter(user=user)
                        context = {'check_in':check_in,'check_out':check_out,'room':room,'room_no':room_no,'price':price,'coupon':coupon,'coupen_exist':True,'paypal_price':paypal_price,'razorpay_price':razorpay_price}
                        return render(request,'user/book.html',context)
                    
                else:
                    context = {'check_in':check_in,'check_out':check_out,'room':room,'room_no':room_no,'price':price,'paypal_price':paypal_price,'razorpay_price':razorpay_price}
                    return render(request,'user/book.html',context)
            else:
                return redirect(home)
    else:
        return redirect(home)


def view_coupen(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect(home)
        else:
            user = request.user 
            if Coupen.objects.filter(user=user).exists():
                coupon = Coupen.objects.filter(user=user,end__gt=date.today())
                context = {'coupons':coupon}
                return render(request,'user/viewcoupen.html',context)
            else:
                return render(request,'user/viewcoupen.html')
    else:
        return redirect(home)

def check_coupen(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            check_code = request.POST['check_code']
            user = request.user
            if Coupen.objects.filter(code=check_code,user=user).exists():
                coupon = Coupen.objects.get(code=check_code,user=user)
                if coupon.start <= date.today() and coupon.end >= date.today():
                    if coupon.used == False:
                        coupon.used = True
                        coupon.save()
                        request.session['coupon'] = check_code
                        return JsonResponse('true',safe=False) 
                    else:
                        return JsonResponse('used',safe=False)
                else:
                    return JsonResponse('date',safe=False) 
            else:
                return JsonResponse('false',safe=False)
            
        else:
            return redirect(home)
    else:
        return redirect(home)
            
# booking history shown to user
def history(request):
    if request.user.is_authenticated:
        user = request.user
        roompic = RoomPic.objects.all()
        book = BookRoom.objects.filter(user=user)
        for x in book:
            if date.today() > x.check_out:
                x.checked_out = True
                x.save()
        return render(request,'user/history.html', {'booking':book,'roompics':roompic})
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
        check_in = request.POST['check_in']
        roomf = int(request.POST['room'])
        room = RoomOverView.objects.get(category=categoryf)
        userbook = BookRoom.objects.filter(room=room,check_in=check_in)
        no_rooms = 0
        for x in userbook:
            if x.block == False:
                no_rooms += x.no_of_room
        receptionbook = ReceptionBook.objects.filter(room=room,check_in=check_in)
        for x in receptionbook:
            no_rooms += x.no_of_room
        available = room.rooms - no_rooms
        for x in setamenities:
            if x.room == room:
                amenity_list.append(x.amenities.amenities)
        exist = False
        for x in amenity_listf:
            exist = True
        for x in amenity_listf:
            if x in amenity_list:
                flag = True
            else:
                flag = False
        if available >= roomf: 
            if exist == True:
                if flag == True:
                    request.session['room_category'] = categoryf
                    return JsonResponse('true',safe=False)
                else:
                    return JsonResponse('amenity',safe=False)
            else:
                request.session['room_category'] = categoryf
                return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        if request.session.has_key('room_category'):
            category1 = request.session['room_category']
            category = Category.objects.get(id = category1)
            room = RoomOverView.objects.get(category=category1)
            roompic = RoomPic.objects.filter(room=room)
            context = {'room':room,'category':category,'amenities':amenities,'setamenities':setamenities,'roompics':roompic}
            return render(request, 'user/filter.html', context)
        else:
            return redirect('/')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)

        