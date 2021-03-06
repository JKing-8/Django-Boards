"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_view
from boards import views
from accounts import views as accounts_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<int:pk>', views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new', views.new_topics, name='new_topics'),
    path('signup/', accounts_view.signup, name='signup'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('reset/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
         name='password_reset'),
    path('settings/password/', auth_view.PasswordChangeView.as_view(template_name='password_change.html')),
    path('settings/password/done/', auth_view.PasswordChangeDoneView.as_view(template_name='password_change.html')),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('new_post/', views.NewPostView.as_view(), name='new_post'),
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('settings/account/',accounts_view.UserUpdateView.as_view(),name='my_account'),
]
