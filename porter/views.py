from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from .forms import ArticlesForm,UserRegistrationForm,SurveyyForm
from . models import Articles,UserLinks
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from . tasks import links_task
import pandas as pd
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes,force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from . tokens import account_activation_token
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
from .webHookutils import webhook_article





import datetime
@login_required
def index(request):
    content_articles = Articles.objects.all()
    if request.method =="POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            
            link = form.save(commit=False)
            link.owner = request.user
           ## add links to users link tables
            UserLinks.objects.create(owner=request.user,links=form.cleaned_data['Article_links'])
            link.save()
            
            return HttpResponseRedirect("/app/")
    
    else:
        form = ArticlesForm()     
        content_articles = Articles.objects.all()
        userLinkTable =   UserLinks.objects.all()
    
    return render(request,"index.html",{"form":form,"articles":content_articles,"userLinkTable":userLinkTable})


@login_required
def delete_articles(request,article_id):
    article = get_object_or_404(Articles,pk=article_id)
    article.delete()
    
    return HttpResponseRedirect("/app/")

@login_required
def process_schedule(request):
    user = request.user
    if request.method == "POST":
       print(request.POST['schedules'])
    
       scheduled_date_time = pd.to_datetime(request.POST['schedules'])
       #links_task(user.id,schedule=scheduled_date_time,owner=user.email)
       links_task.now(request,user.id)
        
    return HttpResponseRedirect("/app/")




def user_registration(request):  
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)  
        if form.is_valid():  
            
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
          
            current_site = get_current_site(request)  
            mail_subject = 'Account Activation'  
            message = render_to_string('registration/acct_activate.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.content_subtype = "html" 
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = UserRegistrationForm()  
    return render(request, 'registration/signup.html', {'form': form})  
    
    
    
    

def acct_activation(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponseRedirect("/login/")  
    else:  
        return HttpResponse('Activation link is invalid!')  
    
    
    
def surveyView(request):
    if request.method == "POST":
        form = SurveyyForm(request.POST)
        
        if form.is_valid():
            firstname = form.cleaned_data['FirstName']
            lastname = form.cleaned_data['LastName']
            gender = form.cleaned_data['Gender']
            email = form.cleaned_data['Email']
            phone = form.cleaned_data['Phone']
            address = form.cleaned_data['Address']
            bio = form.cleaned_data['bio']
            
            surveyData = {
                "Date_subumited":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Firstname":firstname,
                "lastname":lastname,
                "gender":gender,
                "email":email,
                "phone":phone,
                "address":address,
                "bio":bio
            }
            
            print(surveyData)
            webhook_article(surveyData)
            
            return HttpResponseRedirect("/app/survey/")
        
    else:
        form = SurveyyForm()
            
    return render(request,"survey.html",{"form":form})

    
    