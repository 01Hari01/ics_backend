
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class SupplierUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class SupplierUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True,null=False)
    is_admin = models.BooleanField(default=False)
    objects = SupplierUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @staticmethod
    def authenticate(username=None, password=None):
        try:
            user = SupplierUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except SupplierUser.DoesNotExist:
            return None

    def check_password(self, password):
        return super().check_password(password)



class Supplier(models.Model):
    supplier = models.JSONField()



