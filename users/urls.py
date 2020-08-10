from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('<str:username>/', views.UserProfileDetailView.as_view(), name='user_detail'),
    path('<str:username>/update/', views.UserProfileUpdateView.as_view(), name='user_update'),
    path('togglefollow/', views.follow_toggle_view, name='toggle_follow'),
]