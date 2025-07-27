from django.conf import settings
from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model


class MainCategory(models.Model):
    """
    Model for Main Category.
    """
    class Meta:
        verbose_name_plural = 'Main Category'
    
    category_name = models.CharField(max_length=100, unique=True, blank=False)
    image_url = models.ImageField(upload_to='images/support/', blank=True, null=True)

    def __str__(self):
        return self.category_name

class OriginCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Origin Category'
    """
    Model for Origin Category.
    """
    category_name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.category_name

class DifficultyLevelCategory(models.Model):
    """
    Model for Difficulty Level Category.
    """
    class Meta:
        verbose_name_plural = 'Difficulty level category'
    category_name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.category_name

class Recipe(models.Model):
    """
    Model for Recipe.
    """
    title = models.CharField(max_length=100, blank=False)
    sub_title = models.CharField(max_length=255, blank=False)
    ingredients = models.TextField()
    how_to_prepare = models.TextField()
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    origin_category = models.ForeignKey('OriginCategory', on_delete=models.CASCADE, blank=True, null=True)
    difficulty_level = models.ForeignKey('DifficultyLevelCategory', on_delete=models.CASCADE, blank=True, null=True)
    time_to_prepare =  models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_recipes', blank=True)
    small_image = models.ImageField(upload_to='images/small/posts/', blank=True, null=True) 
    large_image = models.ImageField(upload_to='images/large/posts/', blank=True, null=True) 

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """
        Returns the number of likes for the recipe.
        """
        return self.likes.count()

    def average_rating(self):
        """
        Returns the average rating for the recipe using a custom mapping.
        """
        # Define the custom rating mapping
        rating_mapping = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        }

        # Fetch all ratings for this recipe
        ratings = self.ratings.all()
        if ratings.exists():
            # Calculate the total score using the custom mapping
            total_score = sum(rating_mapping[r.rating] for r in ratings)
            average_score = total_score / ratings.count()
            return average_score
        
        return None 
    

class Rating(models.Model):
    """
    Model for Recipe Ratings.
    """
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating value from 0 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')  # Ensure a user can rate a recipe only once

    def __str__(self):
        return f'{self.user.username} rated {self.recipe.title} with {self.rating}'
    

class Comment(models.Model):
    """
    Model for Comments on Recipes.
    """
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    comment_title = models.CharField(max_length=100, default='', blank=False)
    comment = models.TextField(max_length=250, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'