from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
	title = models.CharField(max_length=32)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	room = models.IntegerField()
	text = models.TextField()
	status_variants = (
		('new', 'Новое'),
		('solving', 'На рассмотрении'),
		('solved', 'Решено')
	)

	status = models.CharField(max_length=8, choices=status_variants, default='new')

	fixer = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='fixer',
		null=True,
	)

class UserProfile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
	)
	admin = models.BooleanField()
