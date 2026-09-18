from django.views.generic import TemplateView

from apps.catalog.models import Category, Product
from apps.posters.models import Poster
from apps.services.models import Service


class HomeView(TemplateView):
    template_name = "core/home.html"

   
class AboutView(TemplateView):
    template_name = "core/about.html"
