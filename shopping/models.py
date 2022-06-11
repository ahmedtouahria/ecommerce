import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from .utils import generate_random_code, generate_transform_id
import random
import os
from colorfield.fields import ColorField
from barcode.writer import ImageWriter
import barcode
from io import BytesIO
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator


# get image path for register files
def upload_image_path_receveur(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "User/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_image_path_products(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path_category(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "category/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )
# using a custom user from override django authentication model USER


class UserManager(BaseUserManager):
    def create_user(self, name, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')
        if not name:
            raise ValueError('user must have a name')
        user_obj = self.model(
            name=name,
            phone=phone,
            password=password
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, name, phone, password=None):
        user = self.create_user(
            name,
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, name, phone, password=None):
        user = self.create_user(
            name,
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=20, blank=False,
                            null=False, unique=True)
    password = models.CharField(
        max_length=100, blank=False, null=False, validators=[MinLengthValidator(8)])
    image = models.ImageField(upload_to='media/customers/')
    code = models.CharField(max_length=12)
    point = models.IntegerField(default=0)
    profits = models.FloatField(default=0)
    is_receveur = models.BooleanField(default=False)
    number_of_referalls = models.IntegerField(default=0)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    created_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.code == '':
            code = generate_random_code()
            self.code = code
        super().save(*args, **kwargs)  # Call the real save() method

    def get_full_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


''' Images for banner area '''


class ImageBanner(models.Model):
    image = models.ImageField(upload_to='media/banners/')


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/category/', null=True)

    def __str__(self):
        return self.name


class CategorySub(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='sub_cat')
    image = models.FileField(upload_to='media/category_sub/', null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        CategorySub, on_delete=models.PROTECT, null=True, blank=True)
    price_achat = models.FloatField(
        verbose_name="prix d'achat", null=True, blank=True)
    price = models.FloatField(
        verbose_name="prix de vent", null=True, blank=True)
    profit = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='media/products/')
    available = models.BooleanField(default=True)
    barcode = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    barcode_num = models.CharField(max_length=13, null=True, blank=True)

    @property
    def profits(self):
        return self.price_achat-self.price
    global random_with_N_digits

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)
    # override for save methde

    def save(self, *args, **kwargs):
        new_barcode_number = str(random_with_N_digits(13))
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(new_barcode_number, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.name}.png', File(buffer), save=False)
        if self.barcode_num == "" or self.barcode_num is None or len(self.barcode_num) == 0:
            self.barcode_num = new_barcode_number
            super().save(*args, **kwargs)
        if self.profit is None:
            self.profit = self.price - self.price_achat
            super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(product=self)
        return ratings.count()

    def avg_rating(self):
        # sum of ratings stars  / len of rating hopw many ratings
        sum = 0
        # no of ratings happened to the product
        ratings = Rating.objects.filter(product=self)
        for x in ratings:
            sum += x.stars

        if ratings.count() > 0:
            return int(sum / ratings.count())
        else:
            return 0      # no of ratings happened to the meal

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/products/')


''' -------- PRODUCT LOGIC ----------- '''


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(category='size')

    def colors(self):
        return super(VariationManager, self).filter(category='color')


class Variation(models.Model):
    VAR_CATEGORY = (('size', 'size'), ('color', 'color'),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORY)
    item = models.CharField(max_length=120)

    def __str__(self):
        return self.product.name
    objects = VariationManager()


''' -------- Order LOGIC ----------- '''


class Order(models.Model):
    STATUS = [
        ('Ordered', 'Ordered'),
        ('Processed', 'Processed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=8)
    recommended_by = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name="recommended_by")
    status = models.CharField(
        max_length=100, choices=STATUS, default='Ordered')

    def customer_number(self):
        return self.customer.phone

    def save(self, *args, **kwargs):
        if self.transaction_id == '':
            transaction_id = generate_transform_id()
            self.transaction_id = transaction_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer}-{self.id}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def getItems(self):
        order_items = OrderItem.object.filter(order=self)
        return order_items

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class Rating(models.Model):
    user = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="rate")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()

    def get_user_name(self):
        return self.user.name

    class Meta:
        unique_together = (('user', 'product'),)
        index_together = (('user', 'product'),)

    def __str__(self):
        return f"{self.user.name} rate {self.stars} to {self.product.name}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order}<--to-->{self.address}'


class Favorite(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='favore')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)

    class Meta:
        # to insure the user favore product one time
        unique_together = (('customer', 'product'),)
        index_together = (('customer', 'product'),)
class Conversion(models.Model):
    receveur=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='converte')
    money=models.FloatField()
    
    