from django.db import models
from django.urls import reverse


# Create your models here.
class Category (models.Model):
    category_name = models.CharField (max_length = 75, unique = True)
    slug = models.SlugField (max_length = 100, unique = True) # https://stackoverflow.com/questions/2845080/how-do-i-fix-this-django-error-exception-type-operationalerror-exception-value
    description = models.CharField (max_length = 300, blank = True)
    category_image = models.ImageField (upload_to = 'photos/categories/', blank = True)

    def __str__(self):
        return self.category_name


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args = [self.slug])
