from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError('user ,most have some email address')

        user = self.model(email = self.normalize_email(email), **extra_field)
        # add some validation for password
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user ,most have some email address')

        # user = self.model(email = self.normalize_email(email), password = password)
        user = self.create_user(email , password)
        # add some validation for password
        # user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return  user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField(null=True , blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # admin

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.f_name} {self.l_name}: {self.email} '

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True , blank=True)
    total_seats = models.IntegerField(null=True , blank=True)
    available_seats = models.IntegerField(null=True , blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Seat(models.Model):
    class SeatType(models.TextChoices):
        BUS_TRAIN = 'BU' , _('Bus_train')
        SINGLE = 'SI' , _('Single')
        COMPARTMENT = 'CO' , _('Compartment')

    company = models.ForeignKey(Company , related_name='seats' , on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    type = models.CharField(max_length=2 , choices=SeatType.choices , default=SeatType.SINGLE)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.seat_number}\'th {self.type} seat in {self.company.__str__()} company'

class Reception(models.Model):
    class ReceptionType(models.TextChoices):
        DRINK = 'DR' , _('Drink')
        FOOD = 'FO' , _('Food')
        DESSERT = 'DE' , _('Dessert')

    seat = models.ForeignKey(Seat , related_name='reception' , on_delete=models.CASCADE)
    type = models.CharField(max_length=2 , choices=ReceptionType.choices , default=ReceptionType.DRINK)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.type} for {self.seat.__str__()}'

class Reservation(models.Model):
    class ReservationStatus(models.TextChoices):
        PENDING = 'PE' , _('Pending')
        CONFIRMED = 'CO' , _('Confirmed')
        CANCELED = 'CA' , _('Canceled')

    user = models.ForeignKey(User , related_name='user' , on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='seat', on_delete=models.CASCADE)
    reception = models.ForeignKey(Reception, related_name='reception', on_delete=models.CASCADE)
    buy = models.DateTimeField()
    status = models.CharField(max_length=2 , choices=ReservationStatus.choices , default=ReservationStatus.PENDING)
    total_price = models.DecimalField(max_digits=10 , decimal_places=2)

    def __str__(self):
        return f'Reservation: {self.user.__str__()} -> {self.seat.__str__()} with {self.reception.type}'



