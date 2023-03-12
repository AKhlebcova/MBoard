from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Feedback
from board.forms import PostForm

# Create your views here.
class PostList(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-public_date')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class PostCreate(CreateView):

    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # redirect_field_name = '/accounts/login/'

    # def form_valid(self, form):
    #     user_post = form.save(commit=False)
    #     user_post.post_type = 'at'
    #     redirect_to_post = super().form_valid(form)
    #     send_mail_new_post.apply_async([user_post.id], countdown=5)
    #     return redirect_to_post

