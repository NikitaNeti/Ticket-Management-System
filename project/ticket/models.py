from django.db import models
from django.contrib.auth.models import AbstractUser
from ticket.managers import Usermanager
from django.utils.timezone import now
from django.db.models import Q
from django.core.validators import MinLengthValidator

# Create your models here.
ROLE = (
        ('Agent', 'Agent'),
        ('Subadmin', 'Subadmin'),
        ('User', 'User'),
    )

PRIORITY = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Emergency', 'Emergency'),
    )    

STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Ready-to-dispatch', 'Ready-to-dispatch'),
        ('Dispatched', 'Dispatched'),
        ('Closed', 'Closed'),

    )


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add= True)
    created_by = models.CharField(max_length=255, default='dj')
    updated_at = models.DateField(auto_now= True)
    updated_by = models.CharField(max_length=255, default='dj')


    class Meta:
        abstract = True


class CustomUserModel(BaseModel,AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    # is_email_verified = models.BooleanField(default=False)
    mobile= models.CharField(max_length=10,validators=[MinLengthValidator(10)],null=False, blank=False)
    role = models.CharField(choices=ROLE,max_length =20,null=False,blank=False) 
    profile_pic = models.ImageField(upload_to='profile_pics',null=True, blank=True)
    status = models.BooleanField(default=True)
    object = Usermanager()


    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Ticket(BaseModel):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, limit_choices_to=Q(role='User'))
    mobile= models.CharField(max_length=10,null=False, blank=False)
    assets = models.CharField(max_length =200,blank=False,null=False)
    priority = models.CharField(choices=PRIORITY, max_length =20,blank=False,null=False)
    serial_no = models.CharField(max_length =15,validators=[MinLengthValidator(5)],blank=False,null=False)
    model_no = models.CharField(max_length =15,validators=[MinLengthValidator(5)],blank=False,null=False)
    ticketstatus = models.CharField(choices=STATUS, max_length =20,blank=False,default='Pending')
    assigned_to = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, limit_choices_to=Q(role='Agent'),related_name='assigned_to')

    






     





