from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('user_profile/', views.profile, name='user_profile'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)