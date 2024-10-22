from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)  # Add owner 
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, default=1)  # Add default owner
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    def __str__(self):
        return self.question_text
    class Meta:
        indexes = [
            models.Index(fields=['pub_date']),  # Index on pub_date for faster queries
        ]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
