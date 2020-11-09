from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class PostListView(ListView):
    model=models.post
    template_name='blog/home.html'
    ordering=['-date_posted']
    context_object_name='posts'
    paginate_by=5

class PostDetailView(DetailView):
    model=models.post
    template_name='blog/post_detail.html'
    context_object_name='post'
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model=models.post
    context_object_name='post'
    fields=['title','content']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model=models.post
    context_object_name='post'
    fields=['title','content']
    redirect_field_name='/'
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model=models.post
    context_object_name='post'
    fields=['title','content']
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    success_url='/'
