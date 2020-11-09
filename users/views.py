from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from . import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import models as blog_models
from django.views.generic import ListView

def register(request):
    if request.method=='POST':
        form=forms.register_form(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"{username} has successfuly saved")
            return redirect("login")
        else:
            form=forms.register_form()
    return render(request,'users/register.html',{'form':forms.register_form})

@login_required
def profile_change(request):
    if request.method=='POST':
        u_form=forms.UserUpdateForm(request.POST,instance=request.user)
        p_form=forms.ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Updated")
            return redirect(f"/user/{request.user.username}")
    else:
        u_form=forms.UserUpdateForm(instance=request.user)
        p_form=forms.ProfileUpdateForm(instance=request.user.profile)
        posts=blog_models.post.objects.filter(author=request.user)

    context={
        'u_form':u_form,
        'p_form':p_form,
        'posts':posts
    }
    return render(request,"users/profile_change.html",context)


class ProfileDetailView(ListView):
    model=blog_models.post
    template_name='users/profile.html'
    context_object_name='posts'
    paginate_by=5
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return blog_models.post.objects.filter(author=user).order_by('-date_posted')
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        profile_user=get_object_or_404(User,username=self.kwargs.get('username'))
        context['profile_user']=profile_user
        return context
        