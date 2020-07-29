from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.all_answers, name='all_answers'),
    path('new/', views.create_question, name='new_question'),
    path('edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('delete/<int:pk>/', views.delete_question, name='delete_question'),
]