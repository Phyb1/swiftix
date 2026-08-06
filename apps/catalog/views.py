from django.conf import settings
from django.views.generic import DetailView, ListView

from apps.core.whatsapp import whatsapp_link

from .models import Category, Product


def build_whatsapp_enquiry_link(product):
    message = (
        f"Hi {settings.SITE_NAME}, I'd like to enquire about: {product.name} "
        "(price on ask)."
    )
    return whatsapp_link(message)


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.select_related("category").filter(in_stock=True)
        self.category = None
        slug = self.kwargs.get("slug")
        if slug:
            self.category = Category.objects.filter(slug=slug).first()
            qs = qs.filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_poa:
            context["whatsapp_enquiry_link"] = build_whatsapp_enquiry_link(self.object)
        return context
