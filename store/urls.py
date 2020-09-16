from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name="index"),
    ####
    #user
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('signup/',views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('signout/',views.signout, name="signout"),
    path('addToCart/',views.addToCart, name="addToCart"),
    path('cartItems/',views.cartItems, name="cartItems"),
    path('plusItem/',views.plusItem, name="plusItem"),
    path('minusItem/',views.minusItem, name="minusItem"),
    path('trackOrder/',views.trackOrder, name="trackOrder"),
    path('profile/',views.profile, name="profile"),
    
    #end user
    
    #Brand
    path('insertBrand/', views.insertBrand, name="insertBrand"),
    path('uploadBrand', views.uploadBrand, name="uploadBrand"),
    path('byBrand', views.byBrand, name="byBrand"),
    path('checkoutUpload', views.checkoutUpload, name="checkoutUpload"),
    #end Brand
    
    #Catagory
    path('insertCatagory/', views.insertCatagory, name="insertCatagory"),
    path('uploadCatagory', views.uploadCatagory, name="uploadCatagory"),
    path('byCatagory', views.byCatagory, name="byCatagory"),
    #end Catagory
    
    # Product
    path('insertProduct/', views.insertProduct, name="insertProduct"),
    path('uploadProduct', views.uploadProduct, name="uploadProduct"),
    path('details', views.details, name="details"),
    path('search', views.search, name="search"),
    #end Product

]