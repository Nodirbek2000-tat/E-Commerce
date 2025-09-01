from lib2to3.fixes.fix_has_key import FixHasKey

from django.db import models


from django.utils import timezone
from django.db.models import BooleanField, TextField, ForeignKey
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
Ordinary, Saler = "ordinary", "saler"
UZB, RUS, ENG = "uzb", "rus", "eng"

class Users(AbstractUser):
    profile_picture_url =models.URLField()
    country=models.CharField(max_length=50, null=False, blank=False)
    last_active=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=30, choices=[
        (Ordinary, "Ordinary"),
        (Saler, "Saler")
    ], default=Ordinary)
    language = models.CharField(max_length=20, choices=[
        (UZB, "O'zbek"),
        (RUS, "RUS"),
        (ENG, "ENGLISH")
    ], default=UZB)

    def str(self):
        return f"{self.get_full_name()}"

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(unique=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
            return self.name


class Payment_type(models.Model):
    type=models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.type






class Comment_type(models.Model):
    Afzalliklar=models.TextField()
    Kamchiliklari=models.TextField()
    Izoh=models.TextField()


class Comments(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    comment_text=models.ForeignKey(Comment_type,on_delete=models.CASCADE)
    stars=models.FloatField(default=0)
    reply_seller=models.TextField()
    comment_count=models.PositiveIntegerField(default=0)


# Published sections

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.Status.Published)

class Product(models.Model):


    class Status(models.TextChoices):
        Draft="DF", "Draft"
        Published = "PB","Published"

    name= models.CharField(max_length=250, null=False,blank=False)
    price = models.IntegerField( null=False,blank=False)
    image = models.ImageField(upload_to="products_image/", null=True, blank=True)
    description=TextField(null=False,blank=False)
    slug = models.SlugField(unique=True,blank=True)
    componnent=models.CharField(max_length=100, null=True,blank=True)
    utilizing_role=models.CharField(max_length=100, null=True,blank=True)
    size=models.CharField(max_length=100, null=True,blank=True)
    stock_count=models.IntegerField()
    order_count=models.IntegerField()
    discount=models.IntegerField(null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    orders=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.Draft)
    published_time=models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    published = PublishedManager()
    objects = models.Manager()



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    payment_type=models.ForeignKey(Payment_type,on_delete=models.CASCADE)
    delevering_point=models.CharField(max_length=150,null=False,blank=False)
    buying_count=models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user


# class Saller(models.Model):
#     name=models.CharField(max_length=50,null=False,blank=False)
#     order_count=models.PositiveIntegerField(default=0)
#     stars=models.FloatField(default=0)
#     category=models.ForeignKey(Category,on_delete=models.CASCADE)


# THEY ARE ONLY ANOTHER SECTIONS OF THE WEB

class Contact(models.Model):
    full_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.full_name} - {self.subject}"

class Advertisement(models.Model):
    title=models.CharField(max_length=150)
    slug=models.SlugField(unique=True,blank=True)
    image=models.ImageField(upload_to='advertisements/',null=True,blank=True)
    is_active=models.BooleanField(default=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    click_count=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title










