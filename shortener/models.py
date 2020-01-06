from django.db import models

# Create your models here.
class URL(models.Model) :
    # 원본 url을 unique=True로 설정하여 중복 체크
    url = models.TextField(unique=True)
    shortURL = models.TextField()
    visited = models.IntegerField(default=0)
    copy = models.IntegerField(default=0)