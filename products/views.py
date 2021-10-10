from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
import math
from products.models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.

class ProductDetailsView(DetailView):
    
    def get(self, request, *args, **kwargs):
    
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        
        inventory_choices = [
            (i, str(i)) for i in range(1, self.object.inventory + 1)
        ]
        context["form"] = CartAddProductForm(inventory= inventory_choices)
        return self.render_to_response(context)
    
    queryset = Product.available.all()

class ProductListView(ListView):
    
    category = None
    paginate_by = 6

    def get_queryset(self):
        
        queryset = Product.available.all()

        category_slug = self.kwargs.get("slug")

        if category_slug:
            self.category = get_object_or_404(Category,slug=category_slug)
            queryset = queryset.filter(category=self.category)
        
        return queryset
    
    def get_related_products(self,category_id:int):
        
        queryset = Product.available.filter(category = category_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        if self.category and self.category.related_category:
            
            related_products = self.get_related_products(self.category.related_category)
            context['related_products'] = self.format_related_products(related_products)

        context['categories'] = Category.objects.all()
        return context

    def format_related_products(self,related_products):
        
        related_products_item = []
            
        for count, products in enumerate(related_products):
            arr_index = math.floor(count / 3)
            
            if len(related_products_item) <= arr_index:
                related_products_item.insert(arr_index,[])

            related_products_item[arr_index].append(products)
        
        return related_products_item