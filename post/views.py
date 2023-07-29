from django.views.generic import ListView,DetailView,UpdateView,CreateView,DeleteView
from .models import Post
from django.urls import reverse, reverse_lazy
from .forms import CRUDFROM
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('posts')

  def form_invalid(self,form):
    return self.render_to_response(self.get_context_data(form=form))

class PostList(LoginRequiredMixin,ListView):
  model = Post
  context_object_name = 'posts'
  template_name = 'post/list.html'
  
class PostDetail(LoginRequiredMixin,DetailView):
  model = Post
  context_object_name = 'post'
  template_name = 'post/detail.html'

class PostCreate(LoginRequiredMixin,CreateView):
  model = Post
  form_class = CRUDFROM
  template_name = 'post/form.html'
  success_url = reverse_lazy('posts')

  def form_valid(self, form):
         form.instance.user = self.request.user
         return super(PostCreate,self).form_valid(form)
  
  

class PostUpdate(LoginRequiredMixin,UpdateView):
  model = Post
  form_class = CRUDFROM
  template_name = 'post/form.html'
  success_url = reverse_lazy('posts')

  def form_valid(self, form):
         return super(PostUpdate,self).form_valid(form)


class PostDelete(LoginRequiredMixin,DeleteView):
  model = Post 
  template_name = 'post/delete.html'
  def get_success_url(self):
    return reverse('posts')

