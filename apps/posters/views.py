from django.views.generic import ListView

from .models import Poster


class PosterListView(ListView):
    model = Poster
    template_name = "posters/poster_list.html"
    context_object_name = "posters"
    paginate_by = 12

    def get_queryset(self):
        return Poster.objects.filter(is_active=True)
