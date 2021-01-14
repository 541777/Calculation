from django.urls import path

from calculation import view1


urlpatterns = [
    path('',view1.cal,name='calculation'),
    path('add',view1.add,name='add'),

   ]
