from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CommentForm
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'polls/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'polls/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog-home")


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse("blog-home")


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'polls/about.html', {'title': 'About'})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'polls/add_comment.html'

    def form_valid(self, form):

        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog-home")


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user.id)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))