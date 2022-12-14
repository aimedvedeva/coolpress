from django.urls import path, include
from rest_framework import routers
from press import views
from press.views import DetailCoolUser

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'authors', views.AuthorsViewSet)

urlpatterns = [
    path('authors/', views.authors),
    #path('authors/<int:user_id>', views.user_detail, name='user-detail'),

#    path('authors/<int:pk>/', DetailCoolUser.as_view(), name='user-detail'),
    path('home/', views.home, name='home'),
    path('author/<int:author_id>', views.author_details, name='author-detail'),
    path('posts-old/', views.posts_list, name='posts-list'),
    path('post_details/<int:post_id>', views.post_detail, name='posts-detail'),
    path('post/<int:post_id>/comment-add/', views.add_post_comment, name='comment-add'),
    path('post/update/<int:post_id>', views.post_update, name='post-update'),
    path('post/add/', views.post_create, name='post-create'),
    path('category/add/', views.category_create, name='category-create'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('posts/', views.PostClassBasedListView.as_view(), name='post-list'),
    path('trending_posts/', views.TrendingPostClassBasedListView.as_view(), name='posts_trending_list'),
    path('posts/<slug:category_slug>', views.PostClassFilteringListView.as_view(), name='post-list-filtered-by-category'),
    path('posts/author/<str:post_author_username>', views.PostClassAuthorFilteringListView.as_view(), name='post-list-filtered-by-author'),
    path('api-category/<slug:slug>', views.category_api, name='category-api'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('posts-search/', views.PostSearchListView.as_view(), name='posts-search'),
]