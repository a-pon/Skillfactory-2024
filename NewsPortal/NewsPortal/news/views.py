from django.contrib.auth.models import Group
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Author, Category, Post
from .filters import PostFilter
from .forms import PostForm
from .signals import PostLimitError


class DefaultView(TemplateView):
    template_name = 'flatpages/default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class PostsList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     if self.request.path == '/news/create/':
    #         post.type = 'N'
    #     elif self.request.path == '/articles/create/':
    #         post.type = 'A'
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post_ = Post(
            author=Author.objects.get(id=request.POST['author']),
            header=request.POST['header'],
            content=request.POST['content']
        )
        if self.request.path == '/news/create/':
            post_.type = 'N'
        if self.request.path == '/articles/create/':
            post_.type = 'A'
        post_._categories = request.POST['categories']

        try:
            post_.save()
        except PostLimitError:
            return redirect('/news/limit/')
        else:
            return redirect(f'/news/{post_.id}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit'
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostLimit(TemplateView):
    template_name = 'post_limit.html'


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class CategoryDetail(SingleObjectMixin, ListView):
    template_name = 'category.html'
    ordering = '-time'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['not_subscribed'] = not(self.request.user in self.object.subscribers.all())
        return context

    def get_queryset(self):
        return self.object.post_set.all()


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe_me(request):
    user = request.user
    category_id = request.GET['category_id']
    # if user not in Category.objects.filter(id=category_id).values('subscribers'):
    Category.objects.get(id=category_id).subscribers.add(user)
    return redirect(f'/categories/{category_id}')
