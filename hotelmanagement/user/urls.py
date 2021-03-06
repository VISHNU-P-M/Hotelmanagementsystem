from django.urls import path
from user import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('otpcheck/',views.otp_check,name = 'otp_check'),
    path('varification/',views.varification, name='varification'),
    path('signup/',views.signup, name='signup'),
    path('addidproof/',views.add_id_proof,name = 'add_id_proof'),
    path('filter/',views.filter, name = 'filter'),
    path('specificroom/<int:id>',views.specific_room, name = 'sepecificroom'),
    path('book/',views.book_room, name='bookroom'),
    path('history/',views.history, name='history'),
    path('coupen/',views.view_coupen,name='coupen'),
    path('checkcoupen/',views.check_coupen,name = 'checkcoupen'),
    path('addreview/<int:id>',views.add_review,name='addreview'),
    path('logout/',views.logout, name='logout'),
]