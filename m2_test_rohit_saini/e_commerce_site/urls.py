from django.urls import path
from . import views
from .views import admin,update,home,select_item,cart,checkout,admin_order
urlpatterns = [
    path('',views.none,name='none'),
    path('admin_panal/',admin.as_view(),name='admin'),
    path('create/',views.create,name='create'),
    path('delete/<int:id>',views.delete),
    path('update/<int:id>',update.as_view(),name='update'),
    path('home/',home.as_view(),name='home'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('home/select_item/<int:id>',select_item.as_view(),name='select_item'),
    path('home/cart/',cart.as_view(),name='cart'),
    path('home/cart/delete/<int:id>/',views.delete_cart_product),
    path('home/checkout/',checkout.as_view(),name='checkout'),
    path('home/orders/',views.orders,name='orders'),
    path('admin_panal/orders/',admin_order.as_view(),name='admin_orders'),
]