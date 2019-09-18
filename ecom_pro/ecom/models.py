from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from PIL import Image

CATEGORY_CHOICES = (
    ('gaming','gaming'),
    ('servers', 'servers'),
    ('casual', 'casual use'),
    ('general', 'general')
)

LABEL_CHOICES = (
    ('p','primary'),
    ('e', 'secondary'),
    ('d', 'danger')
)


class item(models.Model):
    title = models.CharField(max_length =100)
    price = models.FloatField(default =100)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length =10)
    labels = models.CharField(choices = LABEL_CHOICES, max_length = 10)
    description = models.TextField()
    image = models.ImageField(default = "default.png", upload_to ='products')
    quantity = models.IntegerField(default =1)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"pk": self.pk})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"pk": self.pk})

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)



class orderitem(models.Model):
    item = models.ForeignKey(item, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
            return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    


class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    items = models.ManyToManyField(orderitem)
    startdate = models.DateTimeField(auto_now_add = True)
    orderdate = models.DateTimeField()
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username