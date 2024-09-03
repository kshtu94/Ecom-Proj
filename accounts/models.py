from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
# Here we create Accounts Model also , as well as 
# We are going to create Account Manager which will handle custom user Model


class MyAccountManager(BaseUserManager):

    # Define some functions ,
    # First Method to create a User
    def create_user(self,first_name , last_name , username , email , password=None):
        # Raise Error , if Mandat Fields not entered
        if not email:
            raise ValueError('User Must have an email address')

        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            # normalize_email --> if u enter any captial letter to your email address , it will make it small
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        
        # set_password --> used for setting the password
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Need to write Function for creating Super User
    def create_superuser(self,first_name , last_name , email , username ,password):
        # So we'll be using above create_user method inside this create_superuser method
        # It will take all details , & create a user , setting all permision req. for super user
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        # Now we need to set all permisions for super user as True
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user




# Currently we created Account Model
# Now we need to Account for SuperAdmin
# Currently we created SuperAdmin & we are logging in with the UserName , we want to override that
# So need to create Model for our Super Admin also
# We also need to tell our Account Model , that we are using MyAccountManager for all these operations

class Account(AbstractBaseUser):
    # For this account Model we require all the relevant fields like as follows -
    first_name      =   models.CharField(max_length=50)
    last_name       =   models.CharField(max_length=50)
    username        =   models.CharField(max_length=50 , unique=True)
    email           =   models.EmailField(max_length=100 , unique=True)   
    phone_number    =   models.CharField(max_length=50)

    # required Fields
    date_joined     =   models.DateTimeField(auto_now_add=True)
    last_login      =   models.DateTimeField(auto_now_add=True)
    is_admin        =   models.BooleanField(default=False)
    is_staff        =   models.BooleanField(default=False)
    is_active       =   models.BooleanField(default=False)
    is_superadmin   =   models.BooleanField(default=False)

    # Currently username is our Login Field
    # But in our case we want to login with the email address
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    # This means when we return account object inside Template it should return Template
    def __str__(self):
        return self.email
    
    # Also need to define mandatory methods
    def has_perm(self,perm , obj=None):
        # So it says , when user is admin , user has all the permisions to do all changes
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    







    
    
