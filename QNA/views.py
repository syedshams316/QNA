from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.


def index(request):
    questions = Question.objects.order_by('created')
    return render(request, 'qna/index.html', {'questions': questions})


# CRUD of question
class CreateQuestionView(LoginRequiredMixin, generic.CreateView):

    form_class = QuestionForm
    template_name = 'qna/new_question.html'
    success_url = 'index'

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


# CRUD of Answer
class CreateAnswerView(LoginRequiredMixin, generic.CreateView):

    form_class = AnswerForm
    template_name = 'qna/new_answer.html'
    success_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = "Write a good Answer : "
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = Question.objects.get(pk=kwargs.get('pk'))
            answer.author = request.user
            answer.save()

        return redirect(self.success_url)


class UpdateAnswerView(LoginRequiredMixin, generic.UpdateView):

    form_class = AnswerForm
    template_name = 'qna/edit_answer.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)


class DeleteAnswerView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'qna/answer_confirm_delete.html'
    context_object_name = 'answer'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)