from django.shortcuts import redirect
from django.urls import reverse

from .constants import PAGINATE_COUNT
from .forms import CommentForm, PostForm
from .models import Comment, Post


class EditContentMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


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


class CommentMixin(RedirectionPostMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentFormMixin(CommentMixin):
    form_class = CommentForm
