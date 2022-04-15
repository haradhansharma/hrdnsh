from django.contrib import admin
from .models import *
from django.contrib.sites.admin import SiteAdmin

@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    list_display = ('title','card','status')

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('title','card','proficiency','practicing_from')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title','card','responsibilities','start_from')
    

class ExtendSiteOfSite(admin.StackedInline):
    model = ExtendSite
    can_delete = False   
class InterestOfSite(admin.TabularInline):
    model = Interest    

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    inlines = [ExtendSiteOfSite, InterestOfSite]    
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(Testimonial)
admin.site.register(ServiceInquery)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','card','slug')
    prepopulated_fields = {'slug': ('title',)}      
admin.site.register(Service, ServiceAdmin)

admin.site.register(EmailTemplate)
class ServiceOfCard(admin.TabularInline):
    model = Service
    extra = 0

@admin.register(Contacts)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','message')
    
class HireMeOfCard(admin.TabularInline):
    model = HireMe
    extra = 0

class CategoryOfPro(admin.TabularInline):
    model = PrCategory
    extra = 0
    
class WorksOfCard(admin.TabularInline):
    model = Works
    extra = 0
    
class SkillsOfCard(admin.TabularInline):
    model = Skills
    extra = 0
    
class ExperienceOfCard(admin.TabularInline):
    model = Experience
    extra = 0

@admin.register(PrCategory)
class PrCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','card')    


class CardAdmin(admin.ModelAdmin):
    list_display = ('card_type','full_name','short_title','slug')
    prepopulated_fields = {'slug': ('card_type',)}
    inlines = [CategoryOfPro, SkillsOfCard, WorksOfCard, ServiceOfCard, HireMeOfCard, ExperienceOfCard]    
admin.site.register(Card, CardAdmin)
