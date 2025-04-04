from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user

class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    annual_income = models.CharField(max_length=100, null=True, blank=True)
    
    risk_level = models.CharField(max_length=50, null=True, blank=True)
    loss_tolerance = models.CharField(max_length=50, null=True, blank=True)
    market_reaction = models.CharField(max_length=50, null=True, blank=True)
    preferred_assets = models.JSONField(null=True, blank=True)
    preferred_sectors = models.JSONField(null=True, blank=True)
    investment_experience = models.CharField(max_length=50, null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def has_perm(self, perm, obj=None):
        """Whether the user has specific permissions"""
        # 超级用户有所有权限
        return self.is_staff

    def has_module_perms(self, app_label):
        """Whether the user has permission to access a specific application"""
        # 超级用户有所有权限
        return self.is_staff

    @property
    def is_superuser(self):
        """Whether it is a superuser"""
        return self.is_staff

    class Meta:
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

class FavoriteStock(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favorite_stocks')
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'symbol')  
        db_table = 'favorite_stocks'
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.email} - {self.symbol}"

class Investment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='investments')
    symbol = models.CharField(max_length=20)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'investments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.symbol} ({self.quantity})" 