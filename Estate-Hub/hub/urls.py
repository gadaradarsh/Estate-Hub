from django.urls import path
from . import views
app_name='hub'

urlpatterns = [
    path('',views.Home,name='Home'),
    path('RegisterPage/', views.RegisterPage, name='RegisterPage'),
    path('LoginPage/', views.LoginPage, name='LoginPage'),
    path('LogoutPage/', views.LogoutPage, name='LogoutPage'),
    path('role_based_redirect/', views.role_based_redirect, name='role_based_redirect'),

    #Admin
    path('DashboardAdmin/',views.DashboardAdmin,name='DashboardAdmin'),

    path('managePropertiesAdmin/',views.managePropertiesAdmin,name='managePropertiesAdmin'),
    path('manageUser/',views.manageUser,name='manageUser'),
    path('reviewAdmin/',views.reviewAdmin,name='reviewAdmin'),
    path('deleteReview/<int:review_id>/', views.deleteReview, name='deleteReview'),
    path('addEstateProperties/', views.addEstateProperties, name='addEstateProperties'),
    path('editProperty/<int:listing_id>/', views.editProperty, name='editProperty'),
    path('deleteProperty/<int:listing_id>/', views.deleteProperty, name='deleteProperty'),
    path('addUser/', views.addUser, name='addUser'),
    path('editUser/<int:user_id>/', views.editUser, name='editUser'),
    path('deleteUser/<int:user_id>/', views.deleteUser, name='deleteUser'),
    
    #Buyer
    path('DashboardBuyer/',views.DashboardBuyer,name='DashboardBuyer'),
    path('favourite/',views.favourite,name='favourite'),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:property_id>/', views.remove_from_favorites, name='remove_from_favorites'),

    path('managePropertiesBuyer/',views.managePropertiesBuyer,name='managePropertiesBuyer'),
    path('reviewBuyer/',views.reviewBuyer,name='reviewBuyer'),
    path('addReview/<int:property_id>/', views.addReview, name='addReview'),

    #Seller
    path('DashboardSeller/',views.DashboardSeller,name='DashboardSeller'),
    path('managePropertiesSeller/',views.managePropertiesSeller,name='managePropertiesSeller'),
    path('addPropertySeller/', views.addPropertySeller, name='addPropertySeller'),
    path('editPropertySeller/<int:listing_id>/', views.editPropertySeller, name='editPropertySeller'),
    path('deletePropertySeller/<int:listing_id>/', views.deletePropertySeller, name='deletePropertySeller'),
    path('reviewSeller/',views.reviewSeller,name='reviewSeller'),
]
