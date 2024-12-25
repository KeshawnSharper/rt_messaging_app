from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.messages, name='messages'),
    path('messages/<str:email>', views.messages, name='messages'),
]
