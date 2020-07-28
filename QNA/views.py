from django.shortcuts import render
from .models import Question

# Create your views here.


def question_list(request):
    questions = Question.objects.order_by('created')
    return render(request, 'qna/question_list.html', {'questions': questions})