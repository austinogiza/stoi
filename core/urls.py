from django.urls import path, include
from . import views 


app_name ='core'
urlpatterns = [
    
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name="contact"),
        path('about-us/', views.AboutView.as_view(), name="about"),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact-success'),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('product/<slug>', views.DetailView.as_view(), name="details" ),
    # path('cart/', views.CartView.as_view(), name="cart" ),
    # path('checkout/', views.CheckoutView.as_view(), name="checkout" ),
          path('wishlist/<slug>/', views.wishlist, name="wishlist"),
      path('wishlist/home/<slug>/', views.wishlist_home, name="wishlist-home"),
      path('add_to_cart/<slug>', views.add_to_cart, name='add-to-cart'),
    #    path('pricing/', views.PricingView.as_view(), name="pricing" ),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',  views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
  path('wishlist/product/<slug>/', views.wishlist_product, name='wishlist-product'),
  path('cart/', views.CartView.as_view(), name='cart'),
   path('checkout/', views.CheckoutView.as_view(), name="checkout" ),
path('payment/receipt/', views.PaystackView.as_view(), name="payment" ),
      path('payment/success/', views.ConfirmView.as_view(), name="pay" ),
        path('payment/failed/', views.FailedView.as_view(), name="pay-failed" ),
         path('search/', views.SearchListView.as_view(), name="search" ),
          path('category/<slug>/', views.CategoryView, name='categoryview'),
]
