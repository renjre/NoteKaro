from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyNotes(models.Model):
    user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    note = models.TextField()
    # link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.note

