from django.shortcuts import render
from django.views import View


class ShopBasePageView(View):
    template_name = 'base.html'

    def get(self, request):
        return render(request, self.template_name)
