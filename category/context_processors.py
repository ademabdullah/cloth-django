from .models import Category

''' returns a dictionary containing
    all category objects'''
    
def menu_links (request):
    links = Category.objects.all()
    return dict(links=links)
