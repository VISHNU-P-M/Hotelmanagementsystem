from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('receptionhome/',views.receptionhome,name='receptionhome'),
    path('filter/',views.filter, name= 'filter'),
    path('roomstatusreception/',views.roomstatus, name = 'roomstatus'),
    path('specificroom/<int:id>',views.specific_room,name = 'specificroom'),
    path('logout/',views.logout,name='logout')
]