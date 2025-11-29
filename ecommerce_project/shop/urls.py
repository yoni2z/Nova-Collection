from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import cosmetics_view, household, sports

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),  # Specific pattern
    path('glass/', views.category_view, {'category_name': 'Glass'}, name='glass'),
    path('electronics/', views.electronics, name='electronics'),
    path('cosmetics/', cosmetics_view, name='cosmetics'),
    path('household/', household, name='household'),
    path('sports/', sports, name='sports'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-now/', views.order_now, name='order_now'),  # Move this line before <str:category_name> pattern
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('<str:category_name>/', views.category_view, name='category_view'),  # Generic pattern should be last
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
