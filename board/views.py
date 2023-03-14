from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Feedback, User
from board.forms import PostForm, FeedbackForm, UpdateProfileForm, UpdateUserForm
from board.filters import FeedFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль отредактирован успешно')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


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


# def get_user(request):
#     user = request.user
#     return user
class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # redirect_field_name = '/posts/'

    def form_valid(self, form):
        user_post = form.save(commit=False)
        user_post.author = self.request.user

        redirect_to_post = super().form_valid(form)
        # send_mail_new_post.apply_async([user_post.id], countdown=5)
        return redirect_to_post


class FeedCreate(LoginRequiredMixin, CreateView):
    form_class = FeedbackForm
    model = Feedback
    template_name = 'feed_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('id')
        context['post'] = Post.objects.get(id=post_id)
        return context

    def form_valid(self, form, **kwargs):
        user_reply = form.save(commit=False)
        post_id = self.kwargs.get('id')
        user_reply.user = self.request.user
        user_reply.post = Post.objects.get(id=post_id)
        user_reply.save()
        # send_mail_new_post.apply_async([user_post.id], countdown=5)
        return HttpResponseRedirect('/posts/')


class FeedPost(LoginRequiredMixin, ListView):
    queryset = Feedback.objects.all().order_by('-message_date')
    template_name = 'feed_post.html'
    context_object_name = 'feeds'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = FeedFilter(self.request.GET, queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def feed_deleter(request, id):
    feedback = Feedback.objects.get(id=id)
    print(feedback)
    feedback.delete()
    return redirect("feed_post")


def feed_updater(request, id):
    feedback = Feedback.objects.get(id=id)
    if feedback.accept == False:
        print(feedback)
        feedback.accept = True
        feedback.save()
        return redirect("feed_post")
    else:
        return HttpResponse('<h2>ВЫ УЖЕ ПРИНИМАЛИ ДАННОЕ СООБЩЕНИЕ</h2>')

# class FeedPostList(LoginRequiredMixin, ListView):
#     model = Feedback
#     template_name = 'feed_post.html'
#     context_object_name = 'feed'
#     paginate_by = 5
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         post_id = self.kwargs.get('id')
#         return queryset.filter(post=post_id)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post'] = Post.objects.get(id=kwargs.get('id'))
#         return context
