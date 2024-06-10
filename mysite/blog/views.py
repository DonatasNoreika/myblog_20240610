from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from .models import Post
from django.views.generic.edit import FormMixin
from .forms import CommentForm

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

