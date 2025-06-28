from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(80)], null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    STATUS_CHOICES = (
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('simple', 'simple')
    )
    status = models.CharField(choices=STATUS_CHOICES, default='simple')
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}, {self.phone_number}'


class Category(models.Model):
    category_image = models.ImageField(upload_to='category_image/')
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=32)
    product_price = models.PositiveIntegerField()
    product_description = models.TextField()
    type_status = models.BooleanField()
    article_number = models.PositiveIntegerField(unique=True)
    product_video = models.FileField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return round(sum(int(r.rating) for r in reviews) / reviews.count(), 1)
        return 0

    def get_count_user(self):
        return self.review_set.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    product_image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return f'{self.product}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.CharField(choices=RATING_CHOICES, default='1')
    comment = models.TextField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'


class Basket(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.basketitem_set.all())


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_total_price(self):
        return self.product.product_price * self.quantity
