from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm

# Create your views here.


def question_list(request):
    questions = Question.objects.order_by('created')
    return render(request, 'qna/question_list.html', {'questions': questions})


def all_answers(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all().order_by('created')
    return render(request, 'qna/all_answers.html',
                  {'question': question, 'answers': answers})


def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'qna/new_question.html', {'form': form})
