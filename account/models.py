from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class PercomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """      
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model that extends AbstractUser.
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    known_name = models.CharField(max_length=60, null=True, blank=True)
    is_api_user = models.BooleanField(default=False)
    RELEGION = (
        ('christianity','Christianity'),
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('judaism', 'Judaism'),
        ('sikhism', 'Sikhism'),
        ('confucianism', 'Confucianism'),
        ('taoism', 'Taoism'),
        ('shinto', 'Shinto'),       
        
    )
    religion = models.CharField(max_length=60, choices=RELEGION, default='islam')
    phone_number = PhoneNumberField(blank=True)
    
    BLOOD_GROUP = (
        ('ab+','AB+'),
        ('ab-', 'AB-'),
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),       
    )
    blood_group = models.CharField(max_length=60, choices=BLOOD_GROUP, default='ab+')
    
    birth_date = models.DateTimeField(null=True, blank=True)
    
    
    @property
    def associated_site_id(self):
        site_id = self.associated_profile.site.id if self.associated_profile else 0
        return site_id

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PercomUserManager()

    def __str__(self):
        return self.email
