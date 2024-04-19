from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    #app_label = models.CharField(max_length=100)

    def __str__(self):
        return self.username
# Create your models here.

class Memo(models.Model):
    text = models.CharField(max_length=500, blank=True, null = True)  # 메모 내용
    time = models.CharField(max_length=50, default = "00:00") # 메모 타임 라인
    #last_updated = models.DateTimeField(auto_now=True)





