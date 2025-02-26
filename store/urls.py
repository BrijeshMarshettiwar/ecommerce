from django.urls import path
from .import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('<int:id>',views.productDetail, name='productDetail'),
    path('signup/',views.SignupPage, name='signup'),
    path('login/',views.LoginPage, name='login'),
    path('logout/',views.LogoutPage, name='logout'),
    path('About',views.AboutusPage,name='About'),
    path('Services',views.ServicesPage, name='Services'),
    path('Contact',views.ContactPage, name='Contact'),
    path('search/',views.search, name='search'),

]