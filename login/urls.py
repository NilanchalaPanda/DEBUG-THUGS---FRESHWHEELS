from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='LandingPage'),
    path('about-us', views.aboutUs, name='About-Us'),
    path('testimonials', views.testimonials, name='Testimonials'),
    path('registration', views.register, name='Register'),

    path('driver', views.driverPage, name='driverPage'),
    path('driverIndex', views.driverIndex, name='driverIndex'),

    path('customer', views.customerPage, name='customerPage'),
    path('customerIndex', views.customerIndex, name='customerIndex'),

    path('farmer', views.farmerPage, name="farmerPage"),
    path('farmerIndex', views.farmerIndex, name="farmerIndex"),
    path('farmerInventory', views.farmerInventory, name="farmerInventory"),

    path('profile', views.profilePage, name='ProfilePage'),
    path('cart', views.cartPage, name='CartPage'),
    path('product', views.productPage, name='ProductPage'),
    path('account', views.accountPage, name='AccountPage'),
    path('orders', views.ordersPage, name='orderPage'),
    path('requests', views.requestsPage, name='requestPage'),
]
