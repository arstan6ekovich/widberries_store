from django_filters import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'sub_category': ['exact'],
            'product_price': ['gte', 'lt'],
        }
