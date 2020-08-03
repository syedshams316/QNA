from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Question, Answer, Comment
from .forms import QuestionForm, AnswerForm, CommentForm

# Create your views here.


# Index view
def index(request):
    questions = Question.objects.order_by('created')
    return render(request, 'qna/index.html', {'questions': questions})


# CRUD of Questions
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


# CRUD of Answers
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


# CRUD of Comments
class CreateCommentView(LoginRequiredMixin, generic.CreateView):

    form_class = CommentForm
    template_name = 'qna/new_comment.html'
    success_url = 'index'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = Answer.objects.get(pk=kwargs.get('pk'))
            comment.author = request.user
            comment.save()

        return redirect(self.success_url)


class UpdateCommentView(LoginRequiredMixin, generic.UpdateView):

    form_class = CommentForm
    template_name = 'qna/edit_comment.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class DeleteCommentView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'qna/comment_confirm_delete.html'
    context_object_name = 'comment'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


@login_required
def answer_up_vote_toggle(request, pk):

    answer = get_object_or_404(Answer, pk=pk)
    if request.user in answer.up_votes.all():
        answer.up_votes.remove(request.user)
    else:
        answer.up_votes.add(request.user)

    return redirect('question_detail', answer.question.pk)


@login_required
def answer_down_vote_toggle(request, pk):

    answer = get_object_or_404(Answer, pk=pk)
    if request.user in answer.down_votes.all():
        answer.down_votes.remove(request.user)
    else:
        answer.down_votes.add(request.user)

    return redirect('question_detail', answer.question.pk)


@login_required
def comment_up_vote_toggle(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.up_votes.all():
        comment.up_votes.remove(request.user)
    else:
        comment.up_votes.add(request.user)

    return redirect('question_detail', comment.answer.question.pk)


@login_required
def comment_down_vote_toggle(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.down_votes.all():
        comment.down_votes.remove(request.user)
    else:
        comment.down_votes.add(request.user)

    return redirect('question_detail', comment.answer.question.pk)

