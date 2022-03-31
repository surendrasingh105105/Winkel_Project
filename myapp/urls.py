from ast import Name
from unicodedata import name
from django.urls import path,include
from . import views


 

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'), # name='name ll be match with url name '
    path('shop/',views.shop, name='shop'),
    path('cart/',views.cart, name='cart'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('single_product/',views.single_product,name="single_product"),
    path('checkout/',views.checkout,name='checkout'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change_password/',views.change_password,name='change_password'),
    path('seller_index/',views.seller_index,name='seller_index'),
    path('seller_add_product/',views.seller_add_product,name='seller_add_product'),
    path('seller_view_product/',views.seller_view_product,name='seller_view_product'),
    path('seller_edit_product/<int:pk>/',views.seller_edit_product,name='seller_edit_product'),
    path('seller_delete_product/<int:pk>/',views.seller_delete_product,name='seller_delete_product'),
    
    # ------------------------- filter in the shop to find perticular size price etc  ---------------------------------------------------
    
    path('collection_men/',views.collection_men,name='collection_men'),
    path('collection_women/',views.collection_women,name='collection_women'),
    path('collection_kids/',views.collection_kids,name='collection_kids'),
    path('category_shirt/',views.category_shirt,name='category_shirt'),
    path('category_tshirt/',views.category_tshirt,name='category_tshirt'),
    path('category_jeans/',views.category_jeans,name='category_jeans'),
    path('size_small/',views.size_small,name='size_small'),
    path('size_medium/',views.size_medium,name='size_medium'),
    path('size_large/',views.size_large,name='size_large'),
    path('color_blue/',views.color_blue,name='color_blue'),
    path('color_black/',views.color_black,name='color_black'),
    path('color_white/',views.color_white,name='color_white'),
    path('color_pink/',views.color_pink,name='color_pink'),
    path('color_green/',views.color_green,name='color_green'),
    path('color_red/',views.color_red,name='color_red'),
    path('color_yellow/',views.color_yellow,name='color_yellow'),
    
    path('product_detail/<int:pk>/',views.product_detail,name='product_detail'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('change_qty/',views.change_qty,name='change_qty'),
    
    #-------------------------------------------------PAYMENT-URL--------------------------------------------------
    path('pay',views.initiate_payment, name='pay'), #name connect with the .html,s action ="pay" 
    path('callback/',views. callback, name='callback'),
    path('myorders/',views.myorders,name='myorders'),
    
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
]