from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import RecipeForm, CommentForm, RatingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import MainCategory, OriginCategory, DifficultyLevelCategory, Recipe, Comment, Rating


def index_page(request):
    """
    View to return the index page
    """
    return render(request, 'index.html')


def about_page(request):
    """
    View to return the about page
    """
    return render(request, 'about.html')


def home_page(request):
    """
    View function to render the home page displaying only featured recipes
    """
    recipes = Recipe.objects.filter(is_featured=True)
    comments = Comment.objects.filter(is_approved=True, is_active=True)
    context = {
        'home_page': True,
        'recipes': recipes,
        'testimonials': comments
    }
    return render(request, 'home.html', context)


def paginate_queryset(queryset, page_number, per_page=9):
    """
    Paginate a queryset and return the page object and paginator.
    """
    paginator = Paginator(queryset, per_page)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj, paginator


def all_recipes(request):
    """
    View function to render a page displaying all recipes with filtering and pagination.
    """
    recipes = Recipe.objects.all()
    main_categories = MainCategory.objects.all()
    origin_categories = OriginCategory.objects.all()
    difficulty_levels = DifficultyLevelCategory.objects.all()

    # Handle filtering
    if request.method == "POST":
        main_category_form = request.POST.get("main_category")
        origin_category_form = request.POST.get("origin_category")
        difficulty_level_form = request.POST.get("difficulty_level")

        if main_category_form:
            recipes = recipes.filter(main_category_id=main_category_form)
        if origin_category_form:
            recipes = recipes.filter(origin_category_id=origin_category_form)
        if difficulty_level_form:
            recipes = recipes.filter(difficulty_level_id=difficulty_level_form)

    # Pagination
    page_number = request.GET.get('page')
    recipes_page, paginator = paginate_queryset(recipes, page_number, per_page=9)

    context = {
        'recipes': recipes_page,
        'main_categories': main_categories,
        'origin_categories': origin_categories,
        'difficulty_levels': difficulty_levels,
        'all_recipes_page': True,
        'page_obj': recipes_page,  # Pass the paginator page object to the template
    }
    return render(request, 'home.html', context)


def recipe_page(request, pk):
    """
    Render the listing recipe page with the specified listing PK.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    average_rating = recipe.average_rating()
    approved_comments = recipe.comments.filter(is_approved=True).order_by('-created_at')
    form = CommentForm()
    rating_form = RatingForm()
    has_rated = request.user.is_authenticated and Rating.objects.filter(recipe=recipe, user=request.user).exists()

    context = {
        'recipe': recipe,
        'form': form,
        'approved_comments': approved_comments,
        'average_rating': average_rating,
        'rating_form': rating_form,
        'has_rated': has_rated,
    }

    return render(request, 'recipe.html', context)


@login_required
def add_recipe(request):
    """
    Render the recipe form page
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Your new recipe has been added successfully!')
            return redirect('recipe_page', pk=recipe.pk)
    else:
        form = RecipeForm()

    context = {
        'form': form,
        'add_recipe': True,
    }
    return render(request, 'add_recipe.html', context)


@login_required
def edit_recipe(request, pk):
    """
    Render the recipe form page for editing an existing recipe.
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your recipe has been updated successfully!')
            return redirect('recipe_page', pk=recipe.pk)
        else:
            messages.error(request, 'Something went wrong. Please check the form.')
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
    }
    return render(request, 'add_recipe.html', context)


@login_required
def delete_recipe(request, pk):
    """
    Handle the deletion of a recipe.
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user != recipe.author and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this recipe.')
        return redirect('recipe_page', pk=pk)

    if request.method == 'POST':
        try:
            recipe.delete()
            messages.success(request, 'Your recipe has been deleted successfully!')
            return redirect('home_page')
        except Exception as e:
            messages.error(request, f'Something went wrong: {e}')
            return redirect('recipe_page', pk=pk)

    return redirect('recipe_page', pk=pk)


@login_required
def add_comment(request, recipe_pk):
    """
    Handle adding a recipe comment
    """
    recipe = get_object_or_404(Recipe, pk=recipe_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully and is awaiting approval.')
            return redirect('recipe_page', pk=recipe.pk)
    else:
        form = CommentForm()

    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe.html', context)


@login_required
def edit_comment(request, pk):
    """
    Handle the editing of an existing comment
    """
    comment = get_object_or_404(Comment, pk=pk)
    recipe = comment.recipe

    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('recipe_page', pk=recipe.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_approved = False
            comment.save()
            messages.success(request, 'Your comment has been updated successfully and is awaiting approval.')
            return redirect('recipe_page', pk=recipe.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommentForm(instance=comment)

    context = {
        'recipe': recipe,
        'form': form,
        'comment': comment,
    }
    return render(request, 'edit-comment.html', context)


@login_required
def delete_comment(request, pk):
    """
    Handle the deletion of a comment.
    """
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('recipe_page', pk=comment.recipe.pk)

    if request.method == 'POST':
        try:
            comment.delete()
            messages.success(request, 'Your comment has been deleted successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: {e}')
        return redirect('recipe_page', pk=comment.recipe.pk)

    return redirect('recipe_page', pk=comment.recipe.pk)


@login_required
@require_POST
def like_recipe(request, recipe_id):
    """
    Handle the like and unlike functionality for recipes.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user

    if recipe.likes.filter(id=user.id).exists():
        recipe.likes.remove(user)
        is_liked = False
    else:
        recipe.likes.add(user)
        is_liked = True

    response_data = {
        'likes_count': recipe.likes.count(),
        'is_liked': is_liked,
    }

    return JsonResponse(response_data)


@login_required
@login_required
def my_favourites(request):
    """
    Handle displaying recipes liked by the current user with pagination.
    """
    user = request.user
    recipes = user.liked_recipes.all()

    # Pagination
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page number is provided
    recipes_page, paginator = paginate_queryset(recipes, page_number, per_page=9)

    context = {
        'recipes': recipes_page,  # Pass the paginated recipes
        'my_favourites_page': True,
        'page_obj': recipes_page,  # Pass the paginator page object to the template
    }

    return render(request, 'home.html', context)


@login_required
def rate_recipe(request, pk):
    """
    Handle rating a recipe by the current user.
    """
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_value = int(rating_form.cleaned_data['rating'])
            user = request.user

            existing_rating = Rating.objects.filter(recipe=recipe, user=user).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.save()
            else:
                Rating.objects.create(
                    recipe=recipe,
                    user=user,
                    rating=rating_value
                )

            messages.success(request, 'Thanks for your feedback!')
            return redirect('recipe_page', pk=pk)
    else:
        rating_form = RatingForm()

    context = {
        'rating_form': rating_form,
        'recipe': recipe,
    }

    return render(request, 'recipe.html', context)