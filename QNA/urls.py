from django.urls import path
from . import views


urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:pk>/', views.all_answers, name='all_answers'),
    path('new/', views.create_question, name='new_question'),
]