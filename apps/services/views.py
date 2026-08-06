from django.conf import settings
from django.views.generic import DetailView, ListView

from apps.core.whatsapp import whatsapp_link

from .models import Service


def build_whatsapp_quote_link(service):
    message = (
        f"Hi {settings.SITE_NAME}, I'd like a quote for: {service.name}. "
        "Please let me know the next steps."
    )
    return whatsapp_link(message)


class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["whatsapp_link"] = build_whatsapp_quote_link(self.object)
        return context
