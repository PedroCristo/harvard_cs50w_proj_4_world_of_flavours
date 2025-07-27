from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('home_page/', views.home_page, name='home_page'),
    path('about_page/', views.about_page, name='about_page'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
    path('recipe/<int:pk>/', views.recipe_page, name='recipe_page'),
    path('add_recipe/', views.add_recipe, name='add_recipe_page'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'), 
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'), 
    path('recipe/<int:recipe_pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('my_favourites/', views.my_favourites, name='my_favourites'),
    path('recipe/<int:pk>/rate/', views.rate_recipe, name='rate_recipe'),
]
