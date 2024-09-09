from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Category

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'  # Ensure this matches the actual path
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})