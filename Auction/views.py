from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from Guser.models import GUser
# Create your views here.
from Item.models import Item, BidSecurity


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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the item object from the context
        item = context['item']

        # Check if the user has paid the security money for this item
        has_paid = False
        if self.request.user.is_authenticated:
            buyer = GUser.objects.get(user=self.request.user)

            has_paid = BidSecurity.get_status(item=item, user=buyer)
            context['security_money'] = item.base_price*0.10

        # Add the has_paid variable to the context
        context['has_paid'] = has_paid

        return context