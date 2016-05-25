from django import forms
from django.forms import ModelForm
from .models import Members, Pets, CampaignRequests, Contact
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth

class MemberForm(UserCreationForm):	
	# email = forms.EmailField(required=True)
	phone = forms.IntegerField()
	avatar = forms.ImageField(required=False)
	MEMBER_ROLE = (
					('T', 'Tesorero'),
					('V', 'Vocal'),
					('M', 'Miembro'),
					)
	member_role = forms.ChoiceField(choices=MEMBER_ROLE,required=True)

	class Meta:
		model = User
		fields = ('__all__')
		exclude = ['last_login','is_superuser','password','groups','user_permissions','is_staff','is_active','date_joined',]
		# exclude = ['last_login','is_superuser','password','groups','user_permissions','is_staff','email','is_active','date_joined',]

	def clean_email(self):
		data = self.cleaned_data['email']
		if Members.objects.filter(user_perfil__email=data).exists():
			raise forms.ValidationError("This email already used")
		return data

class UsersForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name','last_name', 'email',)

class MembersForm(forms.ModelForm):

	class Meta:
		model = Members
		fields = '__all__'
		exclude = ['user_perfil']

class SocialForm(forms.ModelForm):

	class Meta:
		model = UserSocialAuth
		fields = '__all__'
		exclude = ['user','provider','uid','extra_data']

class PetForm(forms.ModelForm):

	class Meta:
		model = Pets
		fields = '__all__'

class CampaignForm(forms.ModelForm):

	class Meta:
		model = CampaignRequests
		fields = '__all__'

class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = '__all__'



