from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_link = models.URLField(max_length=200)

    def __str__(self):
        return self.name
