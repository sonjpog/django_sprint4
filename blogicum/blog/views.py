from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import PAGINATE_COUNT
from .forms import CommentForm, PostForm
from .mixins import EditContentMixin
from .models import Category, Comment, Post, User
from .service import get_general_posts_filter


class ValidationMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RedirectionPostMixin:
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class RedirectionProfileMixin:
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostMixin:
    model = Post


class PostFormMixin(PostMixin):
    form_class = PostForm


class PostListMixin(PostMixin):
    paginate_by = PAGINATE_COUNT


class PostCreateMixin:
    template_name = 'blog/create.html'


class PostIdCreateMixin(PostCreateMixin):
    pk_url_kwarg = 'post_id'


class PostListView(PostListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet[Any]:
        return get_general_posts_filter()


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_related(
            'author',
            'location',
            'category',
        )

    def get_object(self, queryset=None):
        post = get_object_or_404(
            Post.objects.select_related('author', 'location', 'category'),
            pk=self.kwargs.get(self.pk_url_kwarg),
        )

        if post.author != self.request.user and (
            not post.is_published
            or not post.category.is_published
            or post.pub_date > timezone.now()
        ):
            raise Http404

        return post

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        )
        return context


class CategoryListView(PostListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Any]:
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return get_general_posts_filter().filter(category=category)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return context


class PostCreateView(
    LoginRequiredMixin,
    PostFormMixin,
    PostCreateMixin,
    ValidationMixin,
    RedirectionProfileMixin,
    CreateView,
):
    pass


class PostUpdateView(
    EditContentMixin,
    PostFormMixin,
    PostIdCreateMixin,
    RedirectionPostMixin,
    UpdateView,
):
    pass


class PostDeleteView(
    EditContentMixin,
    PostMixin,
    PostIdCreateMixin,
    RedirectionProfileMixin,
    DeleteView,
):

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ProfilePostListView(PostListMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Any]:
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )

        if self.request.user == self.author:
            # Если текущий пользователь является владельцем страницы профиля
            queryset = Post.objects.select_related(
                'author',
                'location',
                'category',
            ).filter(
                author=self.author
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        else:
            queryset = Post.objects.select_related(
                'author',
                'location',
                'category',
            ).filter(
                author=self.author,
                is_published=True,
                pub_date__lte=timezone.now()
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')

        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfileUpdateView(
    LoginRequiredMixin,
    RedirectionProfileMixin,
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


class CommentMixin(RedirectionPostMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentFormMixin(CommentMixin):
    form_class = CommentForm


class CommentCreateView(LoginRequiredMixin, CommentFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            get_general_posts_filter(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CommentUpdateView(EditContentMixin, CommentFormMixin, UpdateView):
    pass


class CommentDeleteView(EditContentMixin, CommentMixin, DeleteView):
    pass
