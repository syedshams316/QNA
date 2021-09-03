from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ValidationError
from django.urls import reverse

from .forms import UserRegistrationForm, UserProfileUpdateForm, UserLoginForm
from .models import User, UserProfile
# Create your views here.


class UserRegistrationView(generic.FormView):

    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = '/'

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name')
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        user, user_profile = UserProfile.objects.create_user_and_profile(
            full_name=full_name, username=username, email=email, password=password)

        login(self.request, user)

        return super().form_valid(form)


class UserLoginView(generic.FormView):

    form_class = UserLoginForm
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('user_detail', args=(self.request.user.username,)))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            error_message = 'username and password do not match'
            return render(self.request, self.template_name,
                          {'form': form, 'error_message': error_message})
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_detail', args=(self.request.user.username,))


def log_out(request):
    logout(request)
    return redirect('/')


class UserProfileDetailView(generic.DetailView):

    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return UserProfile.objects.create_or_get(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class UserProfileUpdateView(generic.View):

    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update.html'

    def get(self, *args, **kwargs):
        user = self.request.user
        form = self.form_class(initial={

            'full_name': user.profile.full_name,
            'username': user.username,
            'email': user.email,
            'bio': user.profile.bio,
        })

        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        user = self.request.user
        form = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.bio = form.cleaned_data.get('bio')
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                user.profile.avatar = avatar
            user.profile.save()
            user.save()
        else:
            raise ValidationError("Invalid form data")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('user_detail', args=(self.request.user.username,))


def follow_toggle_view(request):
    if not request.method == "POST":
        return redirect('/')
    username = request.POST.get('username')
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.create_or_get(request.user)
    user_profile.toggle_follow(user)
    return redirect(request.POST.get('previous_page'))
