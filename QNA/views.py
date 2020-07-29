from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Answer
from .forms import QuestionForm

# Create your views here.


def index(request):
    questions = Question.objects.order_by('created')
    return render(request, 'qna/index.html', {'questions': questions})


# CRUD of question
class CreateQuestionView(LoginRequiredMixin, generic.CreateView):

    form_class = QuestionForm
    template_name = 'qna/new_question.html'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        context = "write a good question " + str(request.user)
        form = self.form_class()
        return render(request, self.template_name, {'context': context, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()

        return redirect(self.success_url)


class QuestionDetailView(generic.DetailView):

    model = Question
    template_name = 'qna/question_detail.html'
    context_object_name = 'question'


class UpdateQuestionView(LoginRequiredMixin, generic.UpdateView):

    form_class = QuestionForm
    template_name = 'qna/edit_question.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)


class DeleteQuestionView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'qna/question_confirm_delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)




