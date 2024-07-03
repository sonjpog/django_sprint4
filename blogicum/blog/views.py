from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from . import mixins
from .forms import CommentForm, PostForm
from .models import Category, Post, User
from .service import get_general_posts_filter


class PostListView(mixins.PostListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet[Any]:
        return get_general_posts_filter()


class PostDetailView(mixins.PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_related(
            'author',
            'location',
            'category',
        )

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author != self.request.user:
            return get_object_or_404(get_general_posts_filter(),
                                     pk=self.kwargs.get(self.pk_url_kwarg)
                                     )
        return post

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        )
        return context


class CategoryListView(mixins.PostListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Any]:
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return get_general_posts_filter(
            queryset=Post.objects.filter(category=category)
        )

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return context


class PostCreateView(
    LoginRequiredMixin,
    mixins.PostFormMixin,
    mixins.PostCreateMixin,
    mixins.ValidationMixin,
    mixins.RedirectionProfileMixin,
    CreateView,
):
    pass


class PostUpdateView(
    mixins.EditContentMixin,
    mixins.PostFormMixin,
    mixins.PostIdCreateMixin,
    mixins.RedirectionPostMixin,
    UpdateView,
):
    pass


class PostDeleteView(
    mixins.EditContentMixin,
    mixins.PostMixin,
    mixins.PostIdCreateMixin,
    mixins.RedirectionProfileMixin,
    DeleteView,
):

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ProfilePostListView(mixins.PostListMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Any]:
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )

        apply_filters = self.request.user != self.author
        return get_general_posts_filter(
            queryset=self.author.posts.select_related(
                'author',
                'location',
                'category',
            ),
            apply_filters=apply_filters
        )

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfileUpdateView(
    LoginRequiredMixin,
    mixins.RedirectionProfileMixin,
    UpdateView,
):
    model = User
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self, queryset=None):
        return self.request.user


class CommentCreateView(
    LoginRequiredMixin,
    mixins.CommentFormMixin,
    CreateView
):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            get_general_posts_filter(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CommentUpdateView(
    mixins.EditContentMixin,
    mixins.CommentFormMixin,
    UpdateView
):
    pass


class CommentDeleteView(
    mixins.EditContentMixin,
    mixins.CommentMixin,
    DeleteView
):
    pass
