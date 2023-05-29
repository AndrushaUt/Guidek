from django.urls import path
from django.conf.urls.static import static
from .views import *
from django.conf import settings
urlpatterns = [
    path('', home, name='home'),
    path('create/', create, name='create_post'),
    path('logout/<int:status>/', logoutaccount, name='logout'),
    path('auth/<int:status>/',auth,name="auth"),
    path('user/',login_home, name='login_home'),
    path('post/<int:post_num>/', view_post, name="view_post"),
    path('all_posts/<int:page>/',all_posts,name='all_posts'),
    path('profile/<slug:username>/<int:page>/',user_page,name='user_page'),
    path('edit/<int:post_num>/',edit,name='edit'),
    path('delete/post/<int:post_num>/',delete_post,name='delete_post'),
    path('delete/comment/<int:comment_num>/',delete_comment,name='delete_comment'),
    path('register/',register,name='register'),
    path('like/<int:post_num>/<int:is_liked>',like_handler,name='like')
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)