from django.db.models import QuerySet, Count
from django.utils import timezone

from .models import Post


def get_general_posts_filter(
    queryset: QuerySet = Post.objects.all(),
    apply_filters: bool = True
) -> QuerySet:
    if apply_filters:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    queryset = queryset.select_related('category').annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')

    return queryset
