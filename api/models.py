from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from .managers import UserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
import secrets  # For generating the token

SURVEY_ANSWERS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
]

MOOD_ANSWERS = [
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
]

ROLE_CHOICES = [
    ('parent', 'parent'),
    ('child', 'child')
]

class User(AbstractUser):
    email = models.EmailField(verbose_name = 'email address', max_length = 255, unique = True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__ (self):
        return self.email or ""
    
class Participant(models.Model):
    id = ShortUUIDField(length = 10, prefix="id_", primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = False, blank = False)
    first_name = models.CharField(max_length=70, null=False, blank=False)
    last_name = models.CharField(max_length=70, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    phone_number = models.CharField(max_length=70, null=True, blank=True)
    role = models.CharField(max_length=70, choices=ROLE_CHOICES, null=False, blank=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Parent(Participant):
    child = models.ManyToManyField(Participant, related_name="parents")
    token = models.CharField(max_length=32, unique=True, null=True, blank=True)  # Token field for parents
    is_linked = models.BooleanField(default=False)  # Is the parent linked to a child?
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Child(Participant):
    token = models.CharField(max_length=32, unique=True, null=True, blank=True)  # Token field for children
    is_linked = models.BooleanField(default=False)  # Is the child linked to a parent?

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name_plural = "Children"
    
class ChatFile(models.Model):
    owner = models.OneToOneField(Participant, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, null=False, blank=False)
    file_data = models.BinaryField(null=False, blank=False)

    def __str__(self):
        return self.file_name
    
class Survey(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    question2_answer = models.CharField(max_length=150, null=False, blank=False)
    question1_answer = models.CharField(max_length=150, null=False, blank=False)
    question3_answer = models.CharField(max_length=150, null=False, blank=False)
    question4_answer = models.CharField(max_length=150, null=False, blank=False)
    question5_answer = models.CharField(max_length=150, null=False, blank=False)
    question6_answer = models.CharField(max_length=150, null=False, blank=False)
    question7_answer = models.CharField(max_length=150, null=False, blank=False)
    question8_answer = models.CharField(max_length=150, null=False, blank=False)
    question9_answer = models.CharField(max_length=150, null=False, blank=False)
    question10_answer = models.CharField(max_length=150, null=False, blank=False)
    """
    There would be stored some kind of answers to the survey
    """

    def __str__(self):
        return "Survey №" + str(self.id) + " for " + self.participant.first_name + " " + self.participant.last_name

class Mood(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    mood = models.IntegerField(choices=MOOD_ANSWERS, null=False, blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Mood of " + self.participant.first_name + " " + self.participant.last_name + " on " + str(self.date)