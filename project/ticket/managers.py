
from django.contrib.auth.base_user import BaseUserManager


class Usermanager(BaseUserManager):

    use_in_migrations = True
    #create a new userview:

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Please provide a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #create superuserview:
    def create_superuser(self,email,password=None,**extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff True')

        return self.create_user(email,password,**extra_fields)  