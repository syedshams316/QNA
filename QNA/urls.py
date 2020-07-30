from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('question/detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('new/question/', views.CreateQuestionView.as_view(), name='new_question'),
    path('question/edit/<int:pk>/', views.UpdateQuestionView.as_view(), name='edit_question'),
    path('question/delete/<int:pk>/', views.DeleteQuestionView.as_view(), name='delete_question'),
    path('new/answer/<int:pk>/', views.CreateAnswerView.as_view(), name='new_answer'),
    path('answer/edit/<int:pk>/', views.UpdateAnswerView.as_view(), name='edit_answer'),
    path('answer/delete/<int:pk>/', views.DeleteAnswerView.as_view(), name='delete_answer')
]