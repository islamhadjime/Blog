
from django.urls import path
from django.contrib.auth.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.auth.views import *
from .views import *


urlpatterns = [
    path('', home, name="home"),
    # {% url 'post_edit' slug=post.slug%}
    # # POSTS

    path("post_add/", AddView.as_view(),name="post_add"),
    path("post/<str:slug>/", DetailView.as_view(),name="detail"),
    # post("edit_post/<str:slug>",DetailPostView.as_view(),name="post_edit")
    # PERSION
    path("accounts/login/", user_login,name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("accounts/register/",RegisterView.as_view() ,name="register"),
    path("accounts/profile/",ProfileView.as_view() ,name="profile"),
    path("accounts/edit_profile/",EditProfileView.as_view(),name="edit_profile"),
    path("accounts/posts/",ListPost.as_view(),name="list_posts"),


    # #   LIST PERSION
    # path("users/", ViewUserView.as_view(),name="view_user"),
    # path("user<str:username>",,name="view_user"),


]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

