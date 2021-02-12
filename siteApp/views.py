from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout,authenticate, login
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import *


class AddView(TemplateView):
    template_name = "siteApp/append_post.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(reverse("login"))
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse('home'))
        else:
            form = PostForm()
        return render(request, self.template_name, {'form':form})




class DetailView(TemplateView):
    template_name = 'siteApp/detail.html'
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return reverse("login")
        try:
            detail = get_object_or_404(Post, slug__iexact=kwargs['slug'])
            return render(request, self.template_name ,{'detail':detail})
        except:
            messages.success(request,u"Ощибка")

def home(request):
    context ={
        "offset_content":True,
        "posts":Post.objects.all()
    }
    return render(request, 'siteApp/home.html',context)



def user_login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect(reverse("profile"))
                else:
                    messages.success(request,"Ошибка зарегистрировались!")
                    return redirect(reverse("home"))
            else:
                messages.success(request,"Не  зарегистрировались!")
                return redirect(reverse("register"))
    else:
        form = LoginForm()
    return render(request,"registration/login.html",{'form':form})



class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
             form = RegisterForm(request.POST)
             if form.is_valid():
                self.create_new_user(form)
                messages.success(request, u"Вы успешно зарегистрировались!")
                return redirect(reverse("login"))
        context = {
            'form':form
        }
        return render(request,self.template_name,context)
    
    def create_new_user(self,form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
            User.objects.create_user(form.cleaned_data['username'],
                                    email,
                                    form.cleaned_data['password'],
                                    first_name = form.cleaned_data['first_name'],
                                    last_name  =form.cleaned_data['last_name'])
                                    



class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)



class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Профиль успешно обновлен!")
                return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None



class ListPost(TemplateView):
    template_name = "siteApp/list.html"


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse("login")
        try:
            
            user = User.objects.get(first_name__iexact = request.user)
            


            return render(request, self.template_name ,{'post_list':user.posts.all()})
        except:
            messages.success(request,u"Ощибка")


