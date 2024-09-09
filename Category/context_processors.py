from .models import Category

def menu_links(request):
    link = Category.objects.all()
    return {'link': link}
