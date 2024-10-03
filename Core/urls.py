from django.contrib import admin
from django.urls import path,include

from Core import views

urlpatterns = [
    path("",views.home,name="home"),
    path('form/',views.add_form,name='add_form'),
    path('get_form/',views.get_form,name="get_form"),
    path('update_form/<int:id>/',views.update_form,name='update_form'),
    path('list_student/',views.list_student,name="list_student"),
    path('show_barecode/<int:student_id>/',views.show_barecode,name="show_barecode"),
]