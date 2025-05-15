from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm, ListingForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .models import Listing, CustomUser, Review, Favorite

def Home(request):
    return render(request, 'index.html')

# User Registration
def RegisterPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('hub:role_based_redirect')
    else:
        form = CustomUserCreationForm()
    return render(request, 'RegisterPage.html', {'form': form})

# User Login
def LoginPage(request):
    form = CustomLoginForm(request=request,data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f"Welcome {user.username}!")
                return redirect('hub:role_based_redirect')
            else:
                messages.error(request,'Invalid username or password.')
                return redirect('hub:LoginPage')   
    return render(request, 'LoginPage.html',{'form': form})


def LogoutPage(request):
    logout(request)
    messages.success(request,"you have successfully logged out.")
    return redirect('hub:LoginPage')

@login_required
def role_based_redirect(request):
    if request.user.is_authenticated:
        user_role = request.user.role

        if user_role == 'admin':
            return redirect('hub:DashboardAdmin')
        elif user_role == 'buyer':
            return redirect('hub:DashboardBuyer')
        elif user_role == 'seller':
            return redirect('hub:DashboardSeller')
    return redirect('hub:LoginPage')    
    
@login_required
def DashboardAdmin(request):
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('hub:Home')
    
    # Get counts for the dashboard
    total_properties = Listing.objects.count()
    total_buyers = CustomUser.objects.filter(role='buyer').count()
    total_sellers = CustomUser.objects.filter(role='seller').count()
    
    context = {
        'total_properties': total_properties,
        'total_buyers': total_buyers,
        'total_sellers': total_sellers,
    }
    return render(request, 'admin/DashboardAdmin.html', context)

@login_required
def managePropertiesAdmin(request):
    listings = Listing.objects.all().order_by('-id')
    return render(request, 'admin/managePropertiesAdmin.html', {'listings': listings})

@login_required
def manageUser(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin/manageUser.html', {'users': users})

@login_required
def reviewAdmin(request):
    # Get all reviews
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'admin/reviewAdmin.html', {'reviews': reviews})

@login_required
def addEstateProperties(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Property listing added successfully!')
            return redirect('hub:managePropertiesAdmin')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ListingForm()
    return render(request, 'admin/addEstateProperties.html', {'form': form})

@login_required
def editProperty(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('hub:managePropertiesAdmin')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'admin/editProperty.html', {'form': form, 'listing': listing})

@login_required
def deleteProperty(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('hub:managePropertiesAdmin')
    return render(request, 'admin/deleteProperty.html', {'listing': listing})

#Buyer
@login_required
def DashboardBuyer(request):
    # Get counts for the dashboard
    total_properties_viewed = Listing.objects.count()  # You might want to track actual views
    favorite_count = Favorite.objects.filter(user=request.user).count()
    review_count = Review.objects.filter(reviewer=request.user).count()
    
    context = {
        'total_properties_viewed': total_properties_viewed,
        'favorite_count': favorite_count,
        'review_count': review_count,
    }
    return render(request, 'buyer/DashboardBuyer.html', context)

@login_required
def favourite(request):
    # Get all favorites for the current user
    favorites = Favorite.objects.filter(user=request.user).select_related('property')
    return render(request, 'buyer/favourite.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    try:
        Favorite.objects.create(user=request.user, property=property)
        messages.success(request, 'Property added to favorites!')
    except:
        messages.info(request, 'Property is already in your favorites.')
    return redirect('hub:managePropertiesBuyer')

@login_required
def remove_from_favorites(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    try:
        favorite = Favorite.objects.get(user=request.user, property=property)
        favorite.delete()
        messages.success(request, 'Property removed from favorites!')
    except Favorite.DoesNotExist:
        messages.error(request, 'Property not found in favorites.')
    return redirect('hub:favourite')

@login_required
def managePropertiesBuyer(request):
    # Get all properties regardless of owner role
    listings = Listing.objects.all().order_by('-id')
    return render(request, 'buyer/managePropertiesBuyer.html', {'listings': listings})

@login_required
def reviewBuyer(request):
    # Get all properties that the buyer has viewed or inquired about
    properties = Listing.objects.all()  # You might want to filter this based on buyer's activity
    return render(request, 'buyer/reviewBuyer.html', {'properties': properties})

@login_required
def addReview(request, property_id):
    property = get_object_or_404(Listing, id=property_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('hub:reviewBuyer')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()
    return render(request, 'buyer/addReview.html', {'form': form, 'property': property})

#Seller
@login_required
def DashboardSeller(request):
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('hub:Home')
    
    # Get seller's properties
    seller_properties = Listing.objects.filter(owner=request.user)
    
    # Count total properties
    total_properties = seller_properties.count()
    
    # Count total reviews for seller's properties
    total_reviews = Review.objects.filter(property__in=seller_properties).count()
    
    # Count active listings (properties with reviews)
    active_listings = seller_properties.filter(reviews__isnull=False).distinct().count()
    
    context = {
        'total_properties': total_properties,
        'total_reviews': total_reviews,
        'active_listings': active_listings,
    }
    
    return render(request, 'seller/DashboardSeller.html', context)

@login_required
def managePropertiesSeller(request):
    # Only show properties owned by the current seller
    listings = Listing.objects.filter(owner=request.user).order_by('-id')
    return render(request, 'seller/managePropertiesSeller.html', {'listings': listings})

@login_required
def addPropertySeller(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Property listing added successfully!')
            return redirect('hub:managePropertiesSeller')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ListingForm()
    return render(request, 'seller/addPropertySeller.html', {'form': form})

@login_required
def editPropertySeller(request, listing_id):
    # Only allow editing own properties
    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('hub:managePropertiesSeller')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'seller/editPropertySeller.html', {'form': form, 'listing': listing})

@login_required
def deletePropertySeller(request, listing_id):
    # Only allow deleting own properties
    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('hub:managePropertiesSeller')
    return render(request, 'seller/deletePropertySeller.html', {'listing': listing})

@login_required
def reviewSeller(request):
    # Get all properties owned by the seller
    properties = Listing.objects.filter(owner=request.user)
    return render(request, 'seller/reviewSeller.html', {'properties': properties})

@login_required
def addUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('hub:manageUser')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin/addUser.html', {'form': form})

@login_required
def editUser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('hub:manageUser')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'admin/editUser.html', {'form': form, 'user': user})

@login_required
def deleteUser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('hub:manageUser')
    return render(request, 'admin/deleteUser.html', {'user': user})

@login_required
def deleteReview(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Only allow admin to delete reviews
    if request.user.role == 'admin':
        if request.method == 'POST':
            review.delete()
            messages.success(request, 'Review deleted successfully!')
            return redirect('hub:reviewAdmin')
        return render(request, 'admin/deleteReview.html', {'review': review})
    else:
        messages.error(request, 'You do not have permission to delete reviews.')
        return redirect('hub:Home')