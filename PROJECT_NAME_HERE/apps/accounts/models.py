from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rolepermissions.roles import assign_role, clear_roles

from apps.core.constants import database_keys as dk

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and save a user with given email and password.
        """

        if not email:
            raise ValueError('Email is Required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'),  max_length=30, blank=True)
    date_joined = models.DateField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    mobile = models.TextField(max_length=10)
    gender = models.TextField(
        _('gender'), choices=gender_choices, null=True, blank=True)
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)

    last_active = models.DateTimeField(auto_now=True)

    objects = UserManager()

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return "%s (id: %s)" % (self.get_full_name(), self.id)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name of user.
        '''
        return self.first_name

    def get_absolute_url(self):
        return reverse('dashboard:edit-user', args=[self.id])

    def change_user_role(self, roles):
        """Changes User Role

        Requires: django-rolepermissions
        Params:
            user: User Object
            roles: A list containing new roles of the user

        This methods clears the previous roles of the user and replaces them with the new one.
        """

        clear_roles(self)
        for role in roles:
            assign_role(self, role)
        return self

    @staticmethod
    def filter_user_data(search="", sort_by="", sort_order="asc", page=1, page_size=20):
        """Filter the User Queryset and returns it

        Params:
            search (""): String to match in columns (first_name, last_name, email, address, gender, mobile)
            sort_by (""): Column to sort the data by. Throws TypeError if not String, ValueError if column name not matches with any field.
            sort_order (""): 'asc' for ascending or 'dsc' for descending. Orders in Ascending order if nothing is provided.
            start (-1): Start index for sorted data. Throws TypeError if not int or less than -1.
            end (-1): End Index for sorted data. Throws TypeError if not int or less than -1.
        """

        if sort_by == None:
            sort_by = ""

        if type(sort_by) != str:
            raise TypeError(
                "sort_by must be a string, provided " + str(type(sort_by)))

        if sort_by != "":
            if sort_by not in [field.name for field in User._meta.get_fields()]:
                raise ValueError(
                    "Invalid Column Name %s provided for sort_by " % str(sort_by))

        if search == None:
            search = ""

        if type(page) != int or (type(page) == int and page < 1):
            raise TypeError(
                "Page must be a positive integer, provided " + str(type(page)))

        query_filter = Q(first_name__icontains=search) | \
            Q(last_name__icontains=search) | \
            Q(email__icontains=search) | \
            Q(mobile__icontains=search) | \
            Q(gender__icontains=search)

        users = User.objects.filter(query_filter)

        if sort_by != "":
            if sort_order == "asc":
                users = users.order_by(sort_by)
            else:
                users = users.order_by("-"+sort_by)

        start_index = (page-1)*page_size
        total_count = users.count()

        users = users[start_index:start_index+page_size]

        return users, start_index, total_count

    def is_online(self):
        if self.last_active + timezone.timedelta(seconds=300) > timezone.now():
            return True

        return False

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()
