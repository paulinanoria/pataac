from django.conf.urls import include, url, patterns
from .views import home, gallery, about, contact, register, login_member, RegisterMember, signup, members_report_view, pets_report_view, delete_member, delete_pet, update_member, update_pet, detail_pet, update_profile, update_user, add_pet, search, Search, contact_report_view, campaign_request, RequestService, delete_contact, ContactDetailView, adopt, delete_adoption, adoptions_report_view

urlpatterns = [

    url(r'^$', home, name='home'),
    url(r'^search/$', search, name='search'),
    url(r'^signup/$', signup, name='signup'),

    url(r'^gallery/$', gallery, name='gallery'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^register/$', register, name='register'),
    url(r'^login_member/$', login_member, name='login_member'),
    url(r'^add_pet/$', add_pet, name='add_pet'),
    url(r'^request_service/$', campaign_request, name='campaign_request'),

    url(r'^members/$', members_report_view, name='members_report_view'),
    url(r'^pets/$', pets_report_view, name='pets_report_view'),
    url(r'^contacts/$', contact_report_view, name='contact_report_view'),
    url(r'^adoptions/$', adoptions_report_view, name='adoptions_report_view'),
    url(r'^delete_member/(?P<id>\d+)/$', delete_member, name='delete_member'),
    url(r'^delete_pet/(?P<id>\d+)/$', delete_pet, name='delete_pet'),
    url(r'^delete_contact/(?P<id>\d+)/$', delete_contact, name='delete_contact'),
    url(r'^delete_adoption/(?P<id>\d+)/$', delete_adoption, name='delete_adoption'),
    url(r'^detail_member/(?P<id>\d+)/edit/$', update_member, name='update_member'),
    url(r'^detail_pet/(?P<id>\d+)/edit/$', update_pet, name='update_pet'),
    url(r'^detail_pet/(?P<id>\d+)/$', detail_pet, name='detail_pet'),
    url(r'^update_member/(?P<id>\d+)/edit/$', update_profile, name='update_profile'),
    url(r'^update_user/(?P<id>\d+)/edit/$', update_user, name='update_user'),


    url(r'^register_members/$', RegisterMember.as_view(), name='register_members'),
    url(r'^request/$', RequestService.as_view(), name='request'),
    
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'pata_app/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^search_pet/$', Search.as_view(), name='search_pet'),
    url(r'^contact_detail/(?P<pk>[-\d]+)/$', ContactDetailView.as_view(), name='contact_detail'),


    url(r'^adopt/$', adopt, name='adopt'),
]