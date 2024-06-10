from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import Post, Comment
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 5


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form_class = CommentForm

    # success_url = "/"

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.object.pk})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    context_object_name = "comment"

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.kwargs['post_pk']})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "comment_form.html"
    fields = ['content']

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.kwargs['post_pk']})


    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_pk'])
        form.save()
        return super().form_valid(form)


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "my_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)





