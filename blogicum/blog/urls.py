from django.urls import path, include

from . import views

app_name = 'blog'

# Основные URL-шаблоны
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(), name='category_posts'),
]

# URL-шаблоны для постов
posts_urls = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        '<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'
    ),
    path(
        '<int:post_id>/delete/', views.PostDeleteView.as_view(), name='delete_post'
    ),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
]

# URL-шаблоны для комментариев
comments_urls = [
    path('<int:post_id>/comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]

# URL-шаблоны для профиля
profile_urls = [
    path('edit/', views.EditProfileUpdateView.as_view(), name='edit_profile'),
    path(
        '<str:username>/', views.ProfilePostListView.as_view(), name='profile'
    ),
]

# Добавление всех URL-шаблонов в urlpatterns
urlpatterns += [
    path('posts/', include(posts_urls)),
    path('posts/', include(comments_urls)),
    path('profile/', include(profile_urls)),
]
