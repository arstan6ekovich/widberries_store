from django.urls import path, include

from .views import *

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet, basename='users')
router.register(r'review', ReviewView, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('product/', ProductAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('cart/', BasketView.as_view(), name='cart_detail'),
    path('cart_items/', BasketItemView.as_view({'get':'list', 'post':'create'})),
    path('cart_items/<int:pk>/', BasketItemView.as_view({'put':'update','delete':'destroy'}))

]