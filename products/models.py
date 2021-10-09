from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

# Create your models here.

class availableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

class Category(TimeStampedModel):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(unique=True,always_update=False,populate_from="name")
    related_category = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        ordering=("name",)
        verbose_name="Categoria"
        verbose_name_plural="Categorias"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:listByCategory", kwargs={"slug": self.slug})
    
class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,related_name="products",on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True,always_update=False,populate_from="name")
    image = models.ImageField(upload_to="products/%Y,%m,%d",blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    objects = models.Manager()
    available = availableManager()
    
    class Meta:
        ordering=("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})