from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('haircare/', views.haircare, name='haircare'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Product Line pages
    path('lines/vitamin-c/', views.vitamin_c_line, name='vitamin_c_line'),
    path('lines/retinol/', views.retinol_line, name='retinol_line'),
    path('lines/hyaluronic-acid/', views.hyaluronic_acid_line, name='hyaluronic_acid_line'),
    path('lines/skin-whitening/', views.skin_whitening_line, name='skin_whitening_line'),
    path('lines/snail/', views.snail_line, name='snail_line'),
    path('lines/turmeric/', views.turmeric_line, name='turmeric_line'),
    
    # Shop by Category pages (specific product types)
    path('product-type/cleanser/', views.cleanser_category, name='cleanser_category'),
    path('product-type/toner/', views.toner_category, name='toner_category'),
    path('product-type/serum/', views.serum_category, name='serum_category'),
    path('product-type/face-cream/', views.face_cream_category, name='face_cream_category'),
    path('product-type/facial-mask/', views.facial_mask_category, name='facial_mask_category'),
    path('product-type/soap/', views.soap_category, name='soap_category'),
    path('product-type/body-wash/', views.body_wash_category, name='body_wash_category'),
    path('product-type/body-lotion/', views.body_lotion_category, name='body_lotion_category'),
    
    # Shop by Skin Concern pages
    path('concerns/acne-skin/', views.acne_skin_concern, name='acne_skin_concern'),
    path('concerns/aging-skin/', views.aging_skin_concern, name='aging_skin_concern'),
    path('concerns/blackhead-removal/', views.blackhead_removal_concern, name='blackhead_removal_concern'),
    path('concerns/brightening-skin/', views.brightening_skin_concern, name='brightening_skin_concern'),
    path('concerns/dehydrated-skin/', views.dehydrated_skin_concern, name='dehydrated_skin_concern'),
    path('concerns/dry-skin/', views.dry_skin_concern, name='dry_skin_concern'),
    path('concerns/oily-skin/', views.oily_skin_concern, name='oily_skin_concern'),
    path('concerns/soothing-skin/', views.soothing_skin_concern, name='soothing_skin_concern'),
    path('beauty-tools/', views.beauty_tools, name='beauty_tools'),
    
    # Skin Concern URLs
    path('skin-concerns/acne-skin/', views.acne_skin_concern, name='acne_skin_concern'),
    path('skin-concerns/aging-skin/', views.aging_skin_concern, name='aging_skin_concern'),
    path('skin-concerns/blackhead-removal/', views.blackhead_removal_concern, name='blackhead_removal_concern'),
    path('skin-concerns/brightening-skin/', views.brightening_skin_concern, name='brightening_skin_concern'),
    path('skin-concerns/dehydrated-skin/', views.dehydrated_skin_concern, name='dehydrated_skin_concern'),
    path('skin-concerns/oily-skin/', views.oily_skin_concern, name='oily_skin_concern'),
    path('skin-concerns/soothing-skin/', views.soothing_skin_concern, name='soothing_skin_concern'),
] 