from __future__ import unicode_literals
from django.db import models
import re 

class UserManager(models.Manager):
    def register(self, postData):
        #RegEx for email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #RegEx for Password
        PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{5,}$')
        errors = {}

        if len (postData['email']) < 5:
            errors['email'] = "Your email Sucked!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email-invalid'] = 'Invalid Email, Loser!'

        if len(postData['password']) < 5:
            errors['password'] = "Weak-ass Password."
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password-invalid'] = 'Even this password is invalid!'

        if len(postData['password_confirm']) < 5:
            errors['password_confirm'] = 'Comfirm this, Idiot!'
        if postData['password_confirm'] != postData['password']:
            errors['password_match'] = "Your passwords have to match, dhua!"

        return errors

    def login(self, postData):
        messages = []

        if len(postData['email']) < 1:
            messages.append('Wheres the email?!')

        if len(postData['password']) <2:
            messages.append('Wheres the password?!')

        return messages

class ThoughtManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['thought_con']) < 10:
            errors['thought_con'] = "Not enough words to be shared"

        return errors

class User (models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Thought(models.Model):
    thought_con = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ThoughtManager()
    user = models.ForeignKey(User, related_name="thoughts", on_delete = models.CASCADE)
    likes = models.ManyToManyField( User, related_name='liked_thots')

# class Like(models.Model):
#     User
#     Thought
