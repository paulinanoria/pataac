from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from PIL import Image, ImageOps
from social.apps.django_app.default.models import UserSocialAuth

# Create your models here.

class Members(models.Model):
	user_perfil = models.OneToOneField(User, editable=False)
	# member_mail = models.EmailField(unique=True)
	member_phone = models.IntegerField(null=True)
	member_avatar = models.ImageField(upload_to='pata_project/', null=True, blank=True)
	MEMBER_ROLE = (
					('T', 'Tesorero'),
					('V', 'Vocal'),
					('M', 'Miembro'),
					)
	member_role = models.CharField(max_length=1, choices=MEMBER_ROLE, null=True)

	class Meta:
		permissions = (('can_do_member','Can do member'),)
		ordering = ['user_perfil']

	def __unicode__(self):
		return '%s'%(self.user_perfil)

class Pets(models.Model):
	pet_name = models.CharField(max_length=50)
	pet_age = models.PositiveIntegerField(null=True)
	# pet_breed = models.CharField(max_length=50, null=True)
	pet_avatar = models.ImageField(upload_to='pata_project/', null=True, blank=True)
	pet_aggressive = models.BooleanField()
	PET_RESCUED = (
					('R', 'Rescatado'),
					('D', 'Donado'),
					)
	pet_rescued = models.CharField(max_length=1, choices=PET_RESCUED, null=True)
	PET_SPECIE = (
					('P', 'Perro'),
					('G', 'Gato'),
					)
	pet_specie = models.CharField(max_length=1, choices=PET_SPECIE, null=True)
	PET_SEX = (
					('M', 'Macho'),
					('H', 'Hembra'),
					('HE', 'Hembra-Embarazada'),
					('HL', 'Hembra-Lactando'),
					('HM', 'Hembra-Madre'),
					)
	pet_sex = models.CharField(max_length=2, choices=PET_SEX, null=True)
	pet_added = models.DateField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ['pet_name']

	def __unicode__(self):
		return '%s'%(self.pet_name)

class CampaignRequests(models.Model):
	owner = models.ForeignKey(User)
	age = models.PositiveIntegerField()
	address = models.CharField(max_length=50)
	postal_code = models.PositiveIntegerField(null=True)
	identification = models.CharField(max_length=50, null=True)
	phone = models.PositiveIntegerField()
	pet_name = models.CharField(max_length=25)
	PET_SPECIE = (
					('P', 'Perro'),
					('G', 'Gato'),
					)
	pet_specie = models.CharField(max_length=1, choices=PET_SPECIE)
	PET_SEX = (
					('M', 'Macho'),
					('H', 'Hembra'),
					('HE', 'Hembra-Embarazada'),
					('HL', 'Hembra-Lactando'),
					('HM', 'Hembra-Madre'),
					('HM', 'Hembra-Celo'),
					)
	pet_sex = models.CharField(max_length=2, choices=PET_SEX)
	breed = models.CharField(max_length=50)
	color = models.CharField(max_length=50)
	weight = models.PositiveIntegerField(null=True)
	pet_age = models.PositiveIntegerField(null=True)
	pet_aggressive = models.BooleanField()
	diabetes = models.BooleanField()
	cardiac_problems = models.BooleanField()
	tbt = models.BooleanField()
	thyroid = models.BooleanField()
	fleas = models.BooleanField()
	ticks = models.BooleanField()
	additional_data = models.CharField(max_length=50, null=True)	
	date = models.DateField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ['owner']

	def __unicode__(self):
		return '%s - %s'%(self.owner, self.pet)

class Contact(models.Model):
	name = models.CharField(max_length=20)
	mail = models.EmailField()
	subject = models.CharField(max_length=20)
	content = models.TextField(max_length=200)
	date = models.DateField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ['date']

	def __unicode__(self):
		return '%s'%(self.subject)

class Adoptions(models.Model):
	user = models.OneToOneField(UserSocialAuth)
	pet = models.OneToOneField(Pets)
	approved = models.BooleanField(default=False)
	date = models.DateField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ['-date']

	def __unicode__(self):
		return '%s %s'%(self.user, self.pet)


