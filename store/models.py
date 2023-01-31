from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    description = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # related_name='+' => will not create a reverse relationship in Product
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # can create id with next row, otherwise, id  created automatically
    # sku = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.ImageField()
    # store the current time we updated the field
    last_update = models.DateTimeField(auto_now=True)
    # use protect so if we delete a collection we dont delete the products
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # many to many (will appear also in the Promotion class
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    zip = models.PositiveSmallIntegerField(default=0)




class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_created=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_STATUS_PENDING)
    # should not delete orders
    costumer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveSmallIntegerField()
    # one to one field
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    # one to many field
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    crated_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='related_order')
    product = models.ForeignKey(Order, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='related_cart')
    product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
