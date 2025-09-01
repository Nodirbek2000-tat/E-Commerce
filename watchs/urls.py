from django.urls import path
from .views import Home_page,add_news,update_new,delete_new,contact_view,Register_view,Login,Logout,Aksesuar_view
from .views import Speakers_view,Headphones_view,Smart_watches_view,Mobile_phones_view,search_view,about_view,detailed_view,buy_now_view,order_number_view
from .views import add_to_card_views
urlpatterns=[
    path('',Home_page,name='home'),
    path('add/',add_news,name='add_product'),
    path('update/',update_new,name='update_product'),
    path('delete/',delete_new,name='delete_product'),
    path('contact/',contact_view,name="contact_ad"),
    path('login/',Login,name="login_pro"),
    path('logout/',Logout,name="logout_pro"),
    path('register/',Register_view,name="register_pro"),
    path('akses/',Aksesuar_view,name="aksessuar"),
    path('speaker/',Speakers_view,name="speakers"),
    path('headphon/',Headphones_view,name="headphones"),
    path('watches/',Smart_watches_view,name="smart_w"),
    path('phones/',Mobile_phones_view,name="mobile_p"),
    path('search/',search_view,name="searchs"),
    path('about/',about_view,name="about_page"),
    path('detail/<slug:slug>',detailed_view,name="products"),
    path('buy now/<slug:slug>/',buy_now_view,name="buy_now"), #<slug:slug>/
    path('hsbdhcsc/',delete_new,name="add_to_cart"),
    path('order now/',order_number_view,name="orders"),
    path('add to card/',add_to_card_views,name="add_to")
]