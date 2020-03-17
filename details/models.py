from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from department.models import Department

# Create your models here.

class EmployeeManager(BaseUserManager):    # To Support custom user model
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username = username
        )

        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True

        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser):

    email               = models.EmailField(verbose_name='email', max_length=30, unique=True)
    username            = models.CharField(max_length=20, unique=True)
    CHOICES             = [('yes', 'Yes'), ('no', 'No')]
    is_nri              = models.CharField(max_length=20, choices=CHOICES, default='select')
    date_of_birth       = models.DateField(blank=True, null=True)
    dept                = Department.objects.all()
    dept_choices        = [(i.dept_name, i.dept_name) for i in dept]
    dept_name           = models.CharField(max_length=10, choices=dept_choices, default='select')
    gender              = models.CharField(max_length=10, null=True, blank=True)

    #Required fields to implement in order to override built in user model
    date_joined         = models.DateTimeField(verbose_name='date joined', auto_now_add=True)  
    last_login          = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = EmployeeManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
