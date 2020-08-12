import os
from django.db import models
from django.contrib.auth.models import (BaseUserManager, PermissionsMixin,
                                        AbstractBaseUser, UnicodeUsernameValidator)

from . import utils
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_staff_user(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('staff_user must have is_staff True')

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser True')

        return self.create_staff_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='REQUIRED',
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'A user with that username already exists.',
        }
    )

    email = models.EmailField(unique=True, error_messages={
        'unique': 'A user with that email already exists',
        }
    )

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into admin site'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether the user is active.'
                  'UnSelect this instead of deleting account'
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser

        # Enable staff users all the permissions to perform actions
        # in admin site

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_perms(self, perm_list, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class UserProfileManager(models.Manager):

    def create_user_and_profile(self, full_name, username, email, password, **extra_fields):
        if not full_name:
            raise ValueError('full_name must be set ' + str(full_name))

        user = User.objects.create_user(username=username, password=password, email=email)
        user_profile = self.model(user=user, full_name=full_name, **extra_fields)
        user_profile.save()
        return user, user_profile

    def get_or_create(self):
        pass

    def create_or_get(self, user):
        try:
            user_profile = self.get_queryset().get(user=user)
        except models.ObjectDoesNotExist:
            user_profile = self.model(user=user, full_name='dummy-name')
            user_profile.save()
        return user_profile


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField('profile_pic', upload_to=utils.get_image_path,
                               blank=True,
                               default=os.path.join('images', 'profile_pics', 'default-user.jpg'))

    # symmetrical: if A is a friend of B then B is a friend of A
    # since we are defining following and followers we don't want that relation.
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')
    updated = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    def __str__(self):
        return self.full_name

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def follow(self, user):
        user_profile = UserProfile.objects.create_or_get(user)
        self.following.add(user_profile)

    def un_follow(self, user):
        user_profile = UserProfile.objects.create_or_get(user)
        self.following.remove(user_profile)

    def is_following(self, user):
        if self.get_following().filter(user=user).exists():
            return True
        else:
            return False

    def is_followed_by(self, user):
        if self.get_followers().filter(user=user).exists():
            return True
        else:
            return False

    def toggle_follow(self, user):
        if self.is_following(user):
            self.un_follow(user)
        else:
            self.follow(user)
