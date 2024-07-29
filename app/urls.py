from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('generate-blog', views.generate_blog, name='generate-blog'),
    path('blog-list', views.blogs, name='blogs'),
    path('blog-post/<int:pk>/', views.blogs_post, name='blogs-post'),
]