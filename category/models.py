from django.db import models
from django.urls import reverse


''' Category model, each product belongs to a category
    it has a slug (url) attribute and an image attribute
    also
'''

class Category (models.Model):
    category_name = models.CharField (max_length = 75, unique = True)
    slug = models.SlugField (max_length = 100, unique = True) # https://stackoverflow.com/questions/2845080/how-do-i-fix-this-django-error-exception-type-operationalerror-exception-value
    description = models.CharField (max_length = 300, blank = True)
    category_image = models.ImageField (upload_to = 'photos/categories/', blank = True)

    def __str__(self):
        return self.category_name

    ''' The below class is used to overide the database table
        name, without which the table name would be category_category
        (application name followed by model name)
    '''

    class Meta:
        verbose_name = 'category' # name for the object
        verbose_name_plural = 'categories' # a plural name for the object

    ''' The below method is used to perform URL reversing
        note: the args keyword is used to pass a variable number of arguments to a function
        and in this case passes the category slug (i.e. URL) to the view method '''
        
    def get_url(self):
        return reverse('products_by_category', args = [self.slug]) # used to perform URL reversing
