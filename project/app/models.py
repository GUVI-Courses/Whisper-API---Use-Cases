from django.db import models

# Create your models here.
class CodeSnippet(models.Model):
    code = models.TextField()
    documentation=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)