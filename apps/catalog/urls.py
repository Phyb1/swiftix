from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("shop/", views.ProductListView.as_view(), name="product_list"),
    path("shop/category/<slug:slug>/", views.ProductListView.as_view(), name="category_detail"),
    path("shop/item/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
