from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField
    user_name = models.CharField(max_length=20, default='')
    user_address = models.CharField(max_length=100, default='')
    user_email = models.CharField(max_length=30)
    user_password = models.CharField(max_length=16)
    user_phone = models.SmallIntegerField(default=0)
    user_type = models.CharField(max_length=10, default='Farmer')

    def __str__(self):
        return self.user_name

    def get_user_id(self):
        return self.user_id
    
    def get_user_name(self):
        return self.user_name
    
    def get_user_email(self):
        return self.user_email
    
    def get_user_password(self):
        return self.user_password
    
    def get_user_phone(self):
        return self.user_phone
    
    def get_user_type(self):
        return self.user_type

class Customer(models.Model):
    customer_id = models.ForeignKey('login.User', on_delete=models.CASCADE)
    orders = models.SmallIntegerField(default=0)

class Product(models.Model):
    product_id = models.AutoField
    product_type = models.CharField(max_length=20)
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=100)
    product_image = models.ImageField()
    product_price = models.CharField(max_length=5)
    product_quantity = models.SmallIntegerField(default=0)
    product_by = models.ForeignKey('login.User', on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.AutoField
    from_customer = models.ForeignKey('login.Customer', on_delete=models.CASCADE)