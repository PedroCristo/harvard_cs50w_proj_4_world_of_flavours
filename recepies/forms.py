from django import forms
from .models import Recipe, Comment
from django_summernote.widgets import SummernoteWidget

class RecipeForm(forms.ModelForm):
    """
    Form for creating or updating recipes. Includes fields for recipe details
    and uses Summernote widgets.
    """
    class Meta:
        model = Recipe
        fields = [
            'title',
            'sub_title',
            'ingredients',
            'how_to_prepare',
            'main_category',
            'origin_category',
            'difficulty_level',
            'time_to_prepare',
            'small_image',
            'large_image',
        ]
        widgets = {
            'ingredients': SummernoteWidget(),
            'how_to_prepare': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    """
    Form for creating or updating comments. Includes fields for the comment title and content.
    """
    class Meta:
        model = Comment
        fields = ['comment_title', 'comment']

class StarRatingWidget(forms.RadioSelect):
    """
    Custom widget for star rating. Renders radio buttons as star ratings.
    """
    template_name = 'components/star-rating-widget.html'

class RatingForm(forms.Form):
    """
    Form for submitting a rating. Uses the StarRatingWidget to allow users to select a rating from 1 to 5 stars.
    """
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 6)],  # Choices from 1 to 5
        widget=StarRatingWidget(attrs={'class': 'd-flex ml-1'})
    )