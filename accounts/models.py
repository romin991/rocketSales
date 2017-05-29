from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

# Create your models here.
