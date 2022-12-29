from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from Guser.models import GUser
from Item.models import Category
from Item.models import Item
from dashboard.forms import DescForm


@method_decorator(login_required, name='dispatch')
class UserDashboard(DetailView):
    model = GUser;
    context_object_name = 'user_item'
    template_name = "dashboard.html"




@login_required()
def PostItem(request):
    if request.method == "POST":
        print("success")
        print(request.POST)
        user=GUser.check_user(request.user)
        Item.save_item(request,user)
        return redirect('dashboard:mydashboard')
    form = DescForm()
    category=Category.objects.all()
    context={"AllCategory":category,"form":form}

    return render(request,"post-ad.html",context)


