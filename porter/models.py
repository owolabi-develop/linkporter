from django.db import models

from django.conf import settings
from django.db import models
# Create your models here.

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email,password=None):
       
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Articles(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Article_links = models.URLField(verbose_name="Article Links")
    date_added = models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return self.Article_links
    
    

class UserLinks(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    links = models.URLField()
    date_added = models.DateField(auto_now_add=True)
