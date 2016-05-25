from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.forms import ValidationError
from .models import Members, Pets, Contact, Adoptions
# from .forms import User_form, Add_Art_Form
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MemberForm, MembersForm, UsersForm, SocialForm, PetForm, CampaignForm, ContactForm
from django.forms import inlineformset_factory
from django.template import RequestContext
from social.apps.django_app.default.models import UserSocialAuth

 

# Create your views here.

def home(request):
	# print django.apps.apps.get_models()
	return render(request, "pata_app/index.html")

def search(request):
	# print django.apps.apps.get_models()
	return render(request, "pata_app/search.html")

def signup(request):
	return render(request, "pata_app/signup.html")

def gallery(request):
	context = dict()
	context['pets'] = Pets.objects.all().order_by('-id')
	return render(request, "pata_app/gallery.html", context)

def about(request):
	return render(request, "pata_app/about.html")

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST or None)
		if form.is_valid():
			try:
				instance = form.save()
				instance.save()
				return redirect("pata_app:home")
			except:
				print 'An error'
		else:
			form = ContactForm()
			context = { "form": form, 'err': True, }
			return render(request, 'pata_app/contact.html', context)
	else:
		form = ContactForm()
		context = { "form": form, }
		return render(request, 'pata_app/contact.html', context)

def register(request):
	return render(request, "pata_app/register.html")

class RegisterMember(FormView):
	template_name = 'pata_app/register.html'
	form_class = MemberForm
	success_url = reverse_lazy('pata_app:members_report_view')

	def form_valid(self,form):
		user=form.save()
		# new_user = authenticate(username=form.cleaned_data['username'],
		# 							password=form.cleaned_data['password1']
		# 							)
		p = Members()
		p.user_perfil = user
		# p.member_mail = form.cleaned_data['email']
		p.member_phone = form.cleaned_data['phone']
		p.member_role = form.cleaned_data['member_role']
		p.member_avatar = form.cleaned_data['avatar']
		p.save()
		permiso = Permission.objects.get(codename='can_do_member')
		p.user_perfil.user_permissions.add(permiso)
		p.save()
		# login(self.request, new_user)
		return super(RegisterMember,self).form_valid(form)

class RequestService(FormView):
	template_name = 'pata_app/request_service.html'
	form_class = CampaignForm
	success_url = reverse_lazy('pata_app:home')

	def form_valid(self,form):
		return super(RequestService,self).form_valid(form)

def login_member(request):
	if request.method == 'POST':
		username = request.POST['username']
		if '@' in username:
			try:
				username = Members.objects.get(user_perfil__email=username).user_perfil.username
				print username
			except:
				print 'invalid email'
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("pata_app:home")
			else:
				# Return a 'disabled account' error message
				print 'not active'
		else:
			context = { 'err': True, }
			print 'err'
		return render(request, "pata_app/login.html", context)
	else:
		return render(request, "pata_app/login.html")

def members_report_view(request):
	context = dict()
	context['object_list'] = Members.objects.all().order_by('user_perfil__last_name')
	print context['object_list']
	context['users_list'] = UserSocialAuth.objects.all() 
	print UserSocialAuth.objects.all() 
	return render(request, "pata_app/members_report.html", context)

def pets_report_view(request):
	context = dict()
	context['object_list'] = Pets.objects.all().order_by('pet_name')
	return render(request, "pata_app/pets_report.html", context)

def contact_report_view(request):
	context = dict()
	context['object_list'] = Contact.objects.all().order_by('date')
	return render(request, "pata_app/contact_report.html", context)

def adoptions_report_view(request):
	context = dict()
	context['object_list'] = Adoptions.objects.all().order_by('date')
	return render(request, "pata_app/adoptions_report.html", context)

def delete_member(request, id=None):
	member = get_object_or_404(User, id=id)
	member.delete()
	return redirect("pata_app:members_report_view")

def delete_pet(request, id=None):
	pet = get_object_or_404(Pets, id=id)
	pet.delete()
	return redirect("pata_app:pets_report_view")

def delete_contact(request, id=None):
	contact = get_object_or_404(Contact, id=id)
	contact.delete()
	return redirect("pata_app:contact_report_view")

def delete_adoption(request, id=None):
	adoption = get_object_or_404(Adoptions, id=id)
	adoption.delete()
	return redirect("pata_app:adoptions_report_view")

def update_member(request, id=None):
	if request.method == 'POST':
		profile = Members.objects.get(user_perfil_id=id)
		profile_form = MembersForm(data=request.POST, instance=profile)
		profile_user = User.objects.get(id=id)
		users_form = UsersForm(data=request.POST, instance=profile_user)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.user_perfil = User.objects.get(id=id)
			profile.save()
			profile_user = users_form.save(commit=False)
			profile_user.save()
			print profile_user.first_name
			return redirect("pata_app:members_report_view")
		else:
			print profile_form.errors, users_form.errors
	else:
		user = request.user
		profile = Members.objects.get(user_perfil_id=id)
		profile_form = MembersForm(instance=profile)
		profile = User.objects.get(id=id)
		users_form = UsersForm(instance=profile)
	return render(request, "pata_app/manage_members.html", {'profile_form':profile_form, 'users_form':users_form,})

def update_pet(request, id=None):
	if request.method == 'POST':
		pet = Pets.objects.get(id=id)
		pet_form = PetForm(data=request.POST, instance=pet)
		if pet_form.is_valid():
			pet = pet_form.save(commit=False)
			pet.save()
			return redirect("pata_app:pets_report_view")
		else:
			print pet_form.errors, users_form.errors
	else:
		user = request.user
		pet = Pets.objects.get(id=id)
		pet_form = PetForm(instance=pet)
	return render(request, "pata_app/manage_pets.html", {'pet_form':pet_form,})

def update_profile(request, id=None):
	if request.method == 'POST':
		profile = Members.objects.get(user_perfil_id=id)
		profile_form = MembersForm(data=request.POST, instance=profile)
		profile_user = User.objects.get(id=id)
		users_form = UsersForm(data=request.POST, instance=profile_user)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.user_perfil = User.objects.get(id=id)
			profile.save()
			profile_user = users_form.save(commit=False)
			profile_user.save()
			print profile_user.first_name
			return redirect("pata_app:update_profile", id)
		else:
			print profile_form.errors, users_form.errors
	else:
		user = request.user
		profile = Members.objects.get(user_perfil_id=id)
		profile_form = MembersForm(instance=profile)
		profile = User.objects.get(id=id)
		users_form = UsersForm(instance=profile)
	return render(request, "pata_app/manage_members.html", {'profile_form':profile_form, 'users_form':users_form,})

def update_user(request, id=None):
	if request.method == 'POST':
		print id
		profile = UserSocialAuth.objects.get(user_id=id)
		profile_form = SocialForm(data=request.POST, instance=profile)
		profile_user = User.objects.get(id=id)
		users_form = UsersForm(data=request.POST, instance=profile_user)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.user_perfil = User.objects.get(id=id)
			profile.save()
			profile_user = users_form.save(commit=False)
			profile_user.save()
			print profile_user.first_name
			return redirect("pata_app:members_report_view")
		else:
			print profile_form.errors, users_form.errors
	else:
		user = request.user
		profile = UserSocialAuth.objects.get(user_id=id)
		profile_form = SocialForm(instance=profile)
		profile = User.objects.get(id=id)
		users_form = UsersForm(instance=profile)
	return render(request, "pata_app/manage_members.html", {'profile_form':profile_form, 'users_form':users_form,})

def add_pet(request):
	if request.method == 'POST':
		form = PetForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			try:
				instance = form.save()
				instance.save()
				return redirect("pata_app:gallery")
			except:
				print 'An error'
		else:
			form = PetForm()
			context = { "form": form, 'err': True, }
			return render(request, 'pata_app/add_pet.html', context)
	else:
		form = PetForm()
		context = { "form": form, }
		return render(request, 'pata_app/add_pet.html', context)

def detail_pet(request, id=None):
	pet = get_object_or_404(Pets, id=id)
	context = {
		"object_list": "eee",
		"pet": pet,
	}
	return render(request, "pata_app/detail_pet.html", context)

# def adopt_pet(request, id=None, user=None):
	pet = get_object_or_404(Pets, id=id)
	user = get_object_or_404(UserSocialAuth, id=id)
	context = {
		"pet": pet,
		"user": user,
	}
	return render(request, "pata_app/adopt_pet.html", context)

def campaign_request(request):
	if request.method == 'POST':
		form = CampaignForm(request.POST or None)
		if form.is_valid():
			try:
				instance = form.save()
				instance.save()
				return redirect("pata_app:home")
			except:
				print 'An error eee'
		else:
			form = CampaignForm()
			context = { "form": form, 'err': True, }
			return render(request, 'pata_app/request_service.html', context)
	else:
		form = CampaignForm()
		context = { "form": form, }
		return render(request, 'pata_app/request_service.html', context)

class Search(TemplateView):
	template_name = "pata_app/search.html"

	def post(self, request, *arg, **kwargs):
		search = request.POST['q']
		print search
		pets = Pets.objects.filter(pet_name__contains=search)
		print pets
		if pets:
			return render(request, 'pata_app/search.html', {'pets': pets, 'pet': True})
		else:
			return render(request, 'pata_app/search.html', {'pets': pets, 'pet': False})

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'pata_app/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        return context

@login_required
@require_POST
def adopt(request):
	if request.method == 'POST':
		user = request.user.id
		usersocial = UserSocialAuth.objects.get(user_id=user)
		pet_id = request.POST.get('id', None)
		pet = get_object_or_404(Pets, id=pet_id)

		if Adoptions.objects.filter(pet_id=pet_id).exists():
			message = 'You disliked this'
			print 'Already like this'
		else:
			adoption = Adoptions()
			adoption.user = usersocial
			adoption.pet = pet
			adoption.save()
			print 'You love this'
			message = 'You love this'

	ctx = {'message': message}
	# use mimetype instead of content_type if django < 5
	return HttpResponse(json.dumps(ctx), content_type='application/json')




