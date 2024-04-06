from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post,Rebort
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html',context)
class PostListView(ListView):
    model=Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model=Post
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def about(request):
    return render(request,'blog/about.html')
def myreborts(request):
    context={
        'reborts':Rebort.objects.all()
    }
    return render(request, 'blog/myreborts.html', context)
class RebortListView(LoginRequiredMixin,ListView):
    model=Rebort
    template_name = 'blog/myreborts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'reborts'
    ordering = ['-data_rebort']
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
class RebortDetailView(DetailView):
    model=Rebort
    template_name = 'blog/rebort_detail.html'
class RebortCreateView(LoginRequiredMixin, CreateView):
    model = Rebort
    fields = ['city', 'location_latitude', 'location_longitude', 'explanation', 'image', 'solution']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class RebortUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Rebort
    fields=['city', 'location_latitude', 'location_longitude', 'explanation', 'image', 'solution']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class RebortDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Rebort
    success_url = '/myreborts/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class RebortListViewForM(LoginRequiredMixin, ListView):
    model = Rebort
    template_name = 'blog/myrebortsM.html'
    context_object_name = 'reborts'
    ordering = ['-data_rebort']

    def get_queryset(self):
        # Get the city chosen by the user
        chosen_city = self.request.user.username

        # Filter reports based on the chosen city
        queryset = Rebort.objects.filter(city=chosen_city)

        return queryset
    



def municipality(request):
    
    return render(request, 'blog/municipality.html')
