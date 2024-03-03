from django.urls import path
from .views import product_list, lessons_by_product


urlpatterns = [
    path('api/products/', product_list, name='product_list'),
    path('api/lessons/<int:product_id>/', lessons_by_product, name='lessons_by_product'),
]
