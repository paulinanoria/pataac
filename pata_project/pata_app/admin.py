from django.contrib import admin
from .models import Members, Pets, CampaignRequests, Contact, Adoptions
# Register your models here.


admin.site.register(Members)
admin.site.register(Pets)
admin.site.register(CampaignRequests)
admin.site.register(Contact)
admin.site.register(Adoptions)