from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('new/', views.CreateQuestionView.as_view(), name='new_question'),
    path('edit/<int:pk>/', views.UpdateQuestionView.as_view(), name='edit_question'),
    path('delete/<int:pk>/', views.DeleteQuestionView.as_view(), name='delete_question'),
]