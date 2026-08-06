from django.views.generic import TemplateView

from apps.catalog.models import Category, Product
from apps.posters.models import Poster
from apps.services.models import Service


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.filter(
            in_stock=True, is_featured=True
        ).select_related("category")[:8]
        context["categories"] = Category.objects.all()
        context["services"] = Service.objects.filter(is_active=True)
        context["recent_posters"] = Poster.objects.filter(is_active=True)[:4]
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"
