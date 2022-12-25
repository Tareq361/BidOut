from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from Item.models import Item


class AuctionListView(ListView):
    model = Item;
    paginate_by = 9
    template_name = 'live-auction.html'

    def get_queryset(self):
        return Item.get_active_item(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('page'):
            print("true page")
            context['paginator'].get_page(self.request.GET.get('page'))

        return context

class AuctionDetailsView(DetailView):
    model = Item;
    template_name = 'auction-details.html'