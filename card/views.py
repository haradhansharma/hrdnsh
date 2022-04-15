from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, request
from django_xhtml2pdf.views import PdfMixin
from django.views.generic.detail import DetailView
from .forms import ContactModelForm, ServiceInqueryModelForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import BadHeaderError




def index(request):
    
    #I do not want to access it from context editor
    
    branding = Card.objects.all()[0]    
    
    card_list = Card.objects.all()
    skill_list = Skills.objects.all().order_by('card', 'title')    
    service = Service.objects.all().order_by('card', 'title')    
    professional_card =  Card.objects.filter(card_type__exact = 'professional')
    passionate_card =  Card.objects.filter(card_type__exact = 'passionate')
    
    #to pass data in various block in paralux template
    
    professional_skills_count = Skills.objects.filter(card__exact = card_list[0]).count()
    half_psc = professional_skills_count/2   
    professional_skills_1 = Skills.objects.filter(card__exact = card_list[0])[:half_psc]
    professional_skills_2 = Skills.objects.filter(card__exact = card_list[0])[half_psc+1:]    
    passionate_skills_count = Skills.objects.filter(card__exact = card_list[1]).count()
    half_ptsc = passionate_skills_count/2
    passionate_skills_1 = Skills.objects.filter(card__exact = card_list[1])[:half_ptsc]
    passionate_skills_2 = Skills.objects.filter(card__exact = card_list[1])[half_ptsc+1:]
    
        
    
    
    
    
    context={
        'branding':branding,
        'card_list':card_list,
        'professional_skills_1':professional_skills_1,
        'professional_skills_2':professional_skills_2,
        'passionate_skills_1':passionate_skills_1,
        'passionate_skills_2':passionate_skills_2,
        'professional_card':professional_card,
        'passionate_card':passionate_card,  
        'skill_list':skill_list,
        'service':service,        
    }
    return render(request, 'card/index.html', context=context)



def ContactView(request):       
    if request.method == "POST":              
        form = ContactModelForm(request.POST)         
        if form.is_valid(): 
            # mail parameter   
            param =  ExtendSite.objects.all()[0]
            site_mail= param.email 
            host = param.email_host
            port=param.email_port
            userkey=param.email_host_user
            passkey=param.email_host_pass            
            
            # to user mail
            to_email = form.cleaned_data['email']
            to_name = form.cleaned_data['name']
            e_temp = EmailTemplate.objects.filter(email_type__iexact = 'contact')[0]
            subject = e_temp.to_subject                   
            message = 'Dear '+ to_name + '\n\n' + e_temp.to_message  + '\n\n' + 'Best regards \n\n' + e_temp.signature 
             
            # to admin mail           
            form_subject = 'Contact' + ' "' +  form.cleaned_data['subject'] +'"'                      
            form_message = form.cleaned_data['message'] 
                        
            # sent two mail using new connection
            from django.core import mail
            with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:                
                try:
                    mail.EmailMessage( subject, message, site_mail, [to_email], connection=connection,).send()#to customer
                    mail.EmailMessage(form_subject, form_message, site_mail, [site_mail], connection=connection,).send()#to admin
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            form.save()
            messages.success(request, 'Contact request submitted successfully.')
            return redirect('card:contact')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = ContactModelForm(request.POST)            
    context={
        'form':form,    
        'meta_slogan':'Contact Me' ,
        # 'meta_description': ExtendSite.on_site.all()[0].current_location +', '+  ExtendSite.on_site.all()[0].email +', '+  ExtendSite.on_site.all()[0].phone
    }
    
    return render(request, 'card/contact.html', context)       


class CardListView(generic.ListView):
    model = Card
    context_object_name = 'card_list'    
    queryset = Card.objects.all()
    template_name = 'card/card_list.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet          
        context['meta_slogan'] = 'Get Resume From My Cards'
        context['meta_description'] = "<p> Although I specialize in multiple subjects under the pressure of need, I prefer the following two subjects. What you need to do to download a CV based on the subject you feel the need for is:</p><li>Click on the 'Flip' button on the thematic card.</li> <li>Click on the 'Download Button'.</li> <li>Download PDF.</li>"
         
        
        return context
    
        
    
class CardDetailView(PdfMixin, DetailView):
    model = Card
    template_name = 'card/card_detail.html'    
    
    
        
        
        
class ExperienceListView(generic.ListView):
    model = Experience
    context_object_name = 'experience_list'    
    queryset = Experience.objects.all().order_by('card', 'title') 
    template_name = 'card/experience_list.html'
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet     
        context['meta_slogan'] = 'My Experiences'  
        context['meta_description'] = [d.title for d in self.queryset ]      
        return context
    
    
class ExperienceDetailView(generic.DetailView):
    model = Experience    
    template_name = 'card/experience_detail.html' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet     
        context['meta_slogan'] = "My Experience-" + self.object.title
        context['meta_description'] = self.object.responsibilities
              
        return context
     
    
def tag_detail(request, tag):
    works = Works.objects.filter(Tag__name=tag)
    return render(request, 'card/tag_works.html', {'tag': tag, 'works': works})  

 
def works_list_view(request):
    card = Card.objects.all()    
    work_status = Works.objects.order_by('status').values('status').distinct() 
    context = {
        'card_list': card,
        'work_status':work_status, 
        'meta_slogan':'Some of my works',        
    }
    return render(request, 'card/works_list.html', context=context) 


class WorksDetailView(generic.DetailView):
    model = Works  
    template_name = 'card/works_detail.html'  
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet     
        context['meta_slogan'] = self.object.title
        context['meta_description'] = self.object.description
        context['meta_image'] = self.object.picture        
        return context
    
    
def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)    
    if request.method == "POST":              
        form = ServiceInqueryModelForm(request.POST) 
        if form.is_valid():   
            # mail parameter        
            param =  ExtendSite.objects.all()[0]
            site_mail= param.email 
            host = param.email_host
            port=param.email_port
            userkey=param.email_host_user
            passkey=param.email_host_pass
            
            # to user mail
            to_email = form.cleaned_data['email']
            to_name = form.cleaned_data['name']
            e_temp = EmailTemplate.objects.filter(email_type__iexact = 'service_inquery')[0]
            subject = e_temp.to_subject                   
            message = 'Dear '+ to_name + '\n\n' + e_temp.to_message  + '\n\n' + 'Best regards \n\n' + e_temp.signature
             
            # to admin mail           
            form_subject = 'Service Inquery' + ' "' +  form.cleaned_data['subject'] +'"'                      
            form_message =   form.cleaned_data['message'] 
                        
            # sent two mail using new connection
            from django.core import mail
            with mail.get_connection(host=host, port=port,username=userkey,password=passkey) as connection:                
                try:
                    mail.EmailMessage( subject, message, site_mail, [to_email], connection=connection,).send()#to customer
                    mail.EmailMessage(form_subject, form_message, site_mail, [site_mail], connection=connection,).send()#to admin
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                
            #get designated service type and save form
            obj = form.save(commit=False) 
            obj.service = service
            obj.save()
            messages.success(request, 'Request submitted successfully.')
            return redirect('/#services')            
        else:            
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        # default value to message form
        form = ServiceInqueryModelForm(
            initial={
                'subject':'Iquery about ' + service.title,
                'message': 'Dear Haradhan Sharma,\n \nI need...\n \n \n \n \nBest regards \n \n...........'                
                })  
               
    context ={
        'service': service,
        'form':form,
        'meta_slogan':service.title ,
        'meta_description': service.description      
    }
    return render(request, 'card/service_request.html', context=context)     
    
    

    

   
    
   
    
    
