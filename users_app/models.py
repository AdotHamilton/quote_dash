from django.db import models
import re

from django.db.models.fields.related import ForeignKey, ManyToManyField
# Create your models here
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['first_name'])) < 2:
            errors['first_name'] = 'First name must be at least 3 characters!'
        if (len(postData['last_name'])) < 2:
            errors['last_name'] = 'Last name must be at least 3 characters!'
        if (len(postData['password'])) < 7:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Passwords must match!"
        if len(User.objects.all().filter(email=postData['email'])) == 0 :
            pass
        else:
            errors['email'] = "Account already exists!"   
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors
    def update_validator(self, postData):
        errors = {}
        if (len(postData['first_name'])) < 2:
            errors['first_name'] = 'First name must be at least 3 characters!'
        if (len(postData['last_name'])) < 2:
            errors['last_name'] = 'Last name must be at least 3 characters!'
        if len(User.objects.all().filter(email=postData['email'])) == 0 :
            pass
        elif postData['email'] == User.objects.get(id=postData['id']).email:
            pass
        else:
            errors['email'] = "Email already in use!"   
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if (len(postData['author']) < 2):
            errors['author'] = "Author should be 3 or more characters"
        if (len(postData['quote']) < 10):
            errors['quote'] = 'Quote should be more than 10 characters'
        return errors

class Quotes(models.Model):
    author = models.CharField(max_length=50)
    quote = models.TextField()
    uploaded_by = ForeignKey(User, related_name='quotes_posted', on_delete=models.CASCADE)
    likes = ManyToManyField(User, related_name='users_who_like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
