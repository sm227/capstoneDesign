from django.db import models
from django.contrib.auth.models import User as authUser


# class User(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.username
# # Create your models here.


class Video(models.Model):
    user = models.ForeignKey(authUser, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    thumbnail = models.TextField(null=True)



class Memo(models.Model):
    text = models.CharField(max_length=600, null=True)  # 메모 내용
    user = models.ForeignKey(authUser, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    # current_time = models.IntegerField(default=0, null=True, blank=True)
    # def __str__(self):
    #     return self.text
