from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Feedback
from board.forms import PostForm, FeedbackForm, UpdateProfileForm, UpdateUserForm
from board.filters import FeedFilter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy


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


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        user_post = form.save(commit=False)
        user_post.author = self.request.user

        redirect_to_post = super().form_valid(form)
        return redirect_to_post


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    pk_url_kwarg = 'id'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_del.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('posts_list')


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
        print(user_reply.user, user_reply.post.author)
        if user_reply.user != user_reply.post.author:
            user_reply.save()
            return HttpResponseRedirect('/posts/')
        else:
            return redirect(reverse('post_detail', args=[str(post_id)]))


class FeedPost(LoginRequiredMixin, ListView):
    queryset = Feedback.objects.all().order_by('-message_date')
    template_name = 'feed_post.html'
    context_object_name = 'feeds'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().select_related('post').filter(post__author=self.request.user)
        self.filterset = FeedFilter(self.request.GET, queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def feed_deleter(request, id):
    feedback = Feedback.objects.get(id=id)
    author = feedback.post.author
    user = request.user
    if author == user:
        feedback.delete()
        messages.success(request, 'Сообщение удалено!')
        return redirect("feed_post")
    else:
        messages.error(request, 'Вы не можете удалить данное сообщение!')
        return redirect("feed_post")


@login_required
def feed_updater(request, id):
    feedback = Feedback.objects.get(id=id)
    if feedback.accept == False:
        print(feedback)
        feedback.accept = True
        feedback.save()
        messages.success(request, 'Сообщение принято успешно!')
        return redirect("feed_post")
    else:
        messages.error(request, 'Вы уже принимали данное сообщение!')
        return redirect("feed_post")
