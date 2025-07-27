
def user_image(request):
    """
    Context processor to provide the user's profile image URL globally.
    """
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        return {'user_image': user_profile.user_image.url if user_profile.user_image else None}
    return {'user_image': None}