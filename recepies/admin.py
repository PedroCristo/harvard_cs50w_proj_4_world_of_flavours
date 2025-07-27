from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *

# Define your admin classes here
class MainCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for MainCategory model.
    """
    list_display = ('category_name', 'image_url') 
    search_fields = ('category_name',)


class OriginCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Origin Category model.
    """
    list_display = ('category_name',) 
    search_fields = ('category_name',)


class DifficultyLevelCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Difficulty Level Category model.
    """
    list_display = ('category_name',) 
    search_fields = ('category_name',)


class RecipeAdmin(SummernoteModelAdmin):
    """
    Admin interface for Recepie model.
    """
    list_display = ('title',
                    'sub_title',
                    'main_category',
                    'author',
                    'timestamp',
                    'is_featured',
                    'is_active'
                    )    
    list_editable = ('is_featured',
                       'is_active'
                    )
    
    summernote_fields = ('ingredients',
                         'how_to_prepare'
                         )


class RatingAdmin(admin.ModelAdmin):
    """
    Admin interface for Rating model.
    """
    list_display = ('recipe',
                    'user',
                    'rating',
                    'created_at'
                    ) 
    

class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Rating model.
    """
    list_display = ('recipe',
                    'user',
                    'comment',
                    'created_at',
                    'is_approved',
                    'is_active'
                    ) 
    
    list_editable = ('is_approved',
                     'is_active'
                     )
    

# Register your models and admin classes here
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(OriginCategory, OriginCategoryAdmin)
admin.site.register(DifficultyLevelCategory, DifficultyLevelCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)