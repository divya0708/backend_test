from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class User(models.Model):
	primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user_id = models.CharField(max_length = 20)
	user_name = models.CharField(max_length = 100)
	timezone = models.CharField(max_length = 100)

class ActivityPeriod(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	start_time = models.CharField(max_length = 200)
	end_time = models.CharField(max_length = 200)