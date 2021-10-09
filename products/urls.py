from django.urls import path
from products.views import ProductListView, ProductDetailsView


app_name = "products"

urlpatterns = [
    path("",ProductListView.as_view(),name="list"),
    path("<slug:slug>/", ProductDetailsView.as_view(),name="detail"),
    path("category/<slug:slug>/", ProductListView.as_view(),name="list_by_category"),
]