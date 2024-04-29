from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
# Create your models here.


class Memo(models.Model):
    text = models.CharField(max_length=500)  # 메모 내용
    # time = models.DateTimeField()
    # def __str__(self):
    #     return self.text

