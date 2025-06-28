from .models import *
from modeltranslation.translator import TranslationOptions,register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['category_name']


@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ['subcategory_name']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description')